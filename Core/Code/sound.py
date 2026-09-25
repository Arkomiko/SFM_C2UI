"""
The sequence's sound: its clips mixed into one stereo track.

A session's sound sits on the sound tracks as DmeSoundClips, each pointing at
a file under `sound/` and placed by a time frame like any clip.  Only the
tracks that are not muted play - a shipped film keeps its final mix on one
track and mutes the dialogue, music and effects it was made from.

    mix = mix_sequence(session, library, rate=44100)
    mix.rate, mix.channels, mix.samples      # array('h'), interleaved, -32768..32767
    mix.slice(Time.from_seconds(3), Time.from_seconds(5))

Files are read with `parse_wav`: PCM 8, 16, 24 and 32 bit, 32-bit float and
Microsoft ADPCM (which some of Source's own sounds use), mono or stereo, any
rate; they are resampled and spread to stereo on the way into the mix.  MP3 is
not read - a session that names one is reported as a missing sound rather than
played wrong.  Everything here is standard library only.
"""
from __future__ import annotations

import struct
from array import array
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol

from Core.API.dmx import Element, Time
from Core.API.session import FilmClip, Session, SoundClip

__all__ = ["Wave", "Mix", "parse_wav", "sound_path", "active_sound_clips", "mix_sequence", "PlacedSound"]

#: Source's sound name prefixes: stream flags, not part of the path
SOUND_FLAGS = "*#@><^)}$!?~`+(&"


class SoundSource(Protocol):
    """Anything that hands out sound files by content path."""

    def read_bytes(self, rel: str) -> Optional[bytes]:
        """The file's bytes, or None."""
        ...


@dataclass
class Wave:
    """Decoded audio: interleaved 16-bit samples."""
    rate: int
    channels: int
    samples: array = field(default_factory=lambda: array("h"))
    warnings: List[str] = field(default_factory=list)

    @property
    def frames(self) -> int:
        """Sample frames (one per channel set)."""
        return len(self.samples) // max(1, self.channels)

    @property
    def seconds(self) -> float:
        """Length in seconds."""
        return self.frames / self.rate if self.rate else 0.0


@dataclass
class Mix:
    """A finished stereo mix of a span of time."""
    rate: int
    channels: int
    samples: array
    #: sequence time the mix starts at
    start: Time = Time(0)
    warnings: List[str] = field(default_factory=list)

    @property
    def frames(self) -> int:
        """Sample frames in the mix."""
        return len(self.samples) // max(1, self.channels)

    def slice(self, start: Time, end: Time) -> bytes:
        """Raw little-endian 16-bit bytes of the span [start, end), silence beyond the mix."""
        first = round((start.ticks - self.start.ticks) / Time.PER_SECOND * self.rate)
        last = round((end.ticks - self.start.ticks) / Time.PER_SECOND * self.rate)
        first, last = max(0, first), max(0, last)
        chunk = self.samples[first * self.channels:last * self.channels]
        missing = (last - first) * self.channels - len(chunk)
        raw = chunk.tobytes()
        if missing > 0:
            raw += bytes(missing * 2)
        return raw

    def wav_bytes(self) -> bytes:
        """The whole mix as a .wav file."""
        data = self.samples.tobytes()
        fmt = struct.pack("<HHIIHH", 1, self.channels, self.rate, self.rate * self.channels * 2, self.channels * 2, 16)
        return (b"RIFF" + struct.pack("<I", 4 + 8 + len(fmt) + 8 + len(data)) + b"WAVE"
                + b"fmt " + struct.pack("<I", len(fmt)) + fmt
                + b"data" + struct.pack("<I", len(data)) + data + (b"\0" if len(data) & 1 else b""))


def sound_path(name: str) -> str:
    """A DmeGameSound's `soundname` as a content path: flags off, under `sound/`."""
    name = name.strip().lstrip(SOUND_FLAGS).replace("\\", "/").strip("/")
    if not name:
        return ""
    return name if name.lower().startswith("sound/") else f"sound/{name}"


def parse_wav(data: bytes, name: str = "sound.wav") -> Wave:
    """Decode a RIFF WAVE file to interleaved 16-bit samples."""
    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise ValueError(f"{name}: not a WAVE file")
    fmt = None
    payload = b""
    pos = 12
    while pos + 8 <= len(data):
        fourcc, size = data[pos:pos + 4], struct.unpack_from("<I", data, pos + 4)[0]
        body = data[pos + 8:pos + 8 + size]
        if fourcc == b"fmt " and len(body) >= 16:
            fmt = struct.unpack_from("<HHIIHH", body, 0)
        elif fourcc == b"data":
            payload = body
        pos += 8 + size + (size & 1)
    if fmt is None:
        raise ValueError(f"{name}: no fmt chunk")
    tag, channels, rate, _byte_rate, _align, bits = fmt
    if tag == 0xFFFE and len(body) >= 26:              # WAVE_FORMAT_EXTENSIBLE: the real tag sits in the GUID
        tag = struct.unpack_from("<H", body, 24)[0]
    channels = max(1, channels)
    wave = Wave(rate=rate, channels=channels)
    if tag == 1 and bits == 16:
        wave.samples = array("h", payload[:len(payload) - len(payload) % 2])
    elif tag == 1 and bits == 8:
        wave.samples = array("h", ((b - 128) << 8 for b in payload))
    elif tag == 1 and bits == 24:
        count = len(payload) // 3
        wave.samples = array("h", (struct.unpack_from("<h", payload, i * 3 + 1)[0] for i in range(count)))
    elif tag == 1 and bits == 32:
        ints = array("i", payload[:len(payload) - len(payload) % 4])
        wave.samples = array("h", (v >> 16 for v in ints))
    elif tag == 3 and bits == 32:
        floats = array("f", payload[:len(payload) - len(payload) % 4])
        wave.samples = array("h", (max(-32768, min(32767, int(v * 32767))) for v in floats))
    elif tag == 2:
        wave.samples = _decode_ms_adpcm(payload, channels, fmt[4], name)
    else:
        raise ValueError(f"{name}: unsupported WAVE format tag {tag}, {bits} bits")
    return wave


#: Microsoft ADPCM's fixed predictors, as the format defines them
_ADPCM_COEFFICIENTS = ((256, 0), (512, -256), (0, 0), (192, 64), (240, 0), (460, -208), (392, -232))
_ADPCM_STEPS = (230, 230, 230, 230, 307, 409, 512, 614, 768, 614, 512, 409, 307, 230, 230, 230)


def _decode_ms_adpcm(payload: bytes, channels: int, block_size: int, name: str) -> array:
    """Microsoft ADPCM (format tag 2) to 16-bit samples.

    Source ships some of its sounds this way.  Each block starts with a predictor,
    a delta and two samples per channel, then packs two four-bit nibbles per byte,
    each nibble a correction on the prediction from the two samples before it.
    """
    out = array("h")
    if block_size < 7 * channels:
        raise ValueError(f"{name}: ADPCM block of {block_size} bytes is too small for {channels} channels")
    for start in range(0, len(payload) - block_size + 1, block_size):
        block = payload[start:start + block_size]
        at = 0
        predictor, delta, sample1, sample2 = [], [], [], []
        for _channel in range(channels):
            predictor.append(min(block[at], len(_ADPCM_COEFFICIENTS) - 1))
            at += 1
        for _channel in range(channels):
            delta.append(struct.unpack_from("<h", block, at)[0])
            at += 2
        for _channel in range(channels):
            sample1.append(struct.unpack_from("<h", block, at)[0])
            at += 2
        for _channel in range(channels):
            sample2.append(struct.unpack_from("<h", block, at)[0])
            at += 2
        for channel in range(channels):                # the block opens with the two it carries
            out.append(sample2[channel])
        for channel in range(channels):
            out.append(sample1[channel])
        channel = 0
        for byte in block[at:]:
            for nibble in (byte >> 4, byte & 0x0F):
                c0, c1 = _ADPCM_COEFFICIENTS[predictor[channel]]
                signed = nibble - 16 if nibble > 7 else nibble
                predicted = (sample1[channel] * c0 + sample2[channel] * c1) // 256 + signed * delta[channel]
                value = max(-32768, min(32767, predicted))
                out.append(value)
                delta[channel] = max(16, (_ADPCM_STEPS[nibble] * delta[channel]) // 256)
                sample2[channel] = sample1[channel]
                sample1[channel] = value
                channel = (channel + 1) % channels
    return out


@dataclass
class PlacedSound:
    """One clip's sound on the sequence's time."""
    clip: SoundClip
    path: str
    start: Time
    duration: Time
    offset: Time
    scale: float
    volume: float


def active_sound_clips(sequence: FilmClip) -> List[PlacedSound]:
    """The sound clips that play: on tracks and groups that are not muted, not muted
    themselves, with a sound file named."""
    out: List[PlacedSound] = []
    for group in sequence.track_groups:
        if group.element.get("mute"):
            continue
        for track in group.tracks:
            if track.mute:
                continue
            track_volume = float(track.element.get("volume", 1.0) or 1.0)
            for clip in track.clips:
                if not isinstance(clip, SoundClip) or clip.mute:
                    continue
                path = sound_path(clip.sound_name)
                if not path:
                    continue
                sound = clip.element.get("sound")
                volume = float(sound.get("volume", 1.0)) if isinstance(sound, Element) else 1.0
                frame = clip.time_frame
                out.append(PlacedSound(clip, path, frame.start, frame.duration, frame.offset, frame.scale,
                                       volume * track_volume))
    return out


def mix_sequence(session: Session, source: SoundSource, rate: int = 44100,
                 start: Optional[Time] = None, end: Optional[Time] = None) -> Mix:
    """Mix the active sound clips of the session's sequence into stereo 16-bit at
    `rate`, over [start, end) (the whole sequence when not given)."""
    sequence = session.active_clip
    if sequence is None:
        return Mix(rate, 2, array("h"))
    start = start if start is not None else Time(0)
    end = end if end is not None else sequence.time_frame.duration
    frames = max(0, round((end.ticks - start.ticks) / Time.PER_SECOND * rate))
    mix = Mix(rate, 2, array("h", bytes(frames * 4)), start=start)
    if frames == 0:
        return mix
    accum = [0] * (frames * 2)                     # ints: headroom while summing
    cache: Dict[str, Optional[Wave]] = {}
    for placed in active_sound_clips(sequence):
        wave = cache.get(placed.path, ...)
        if wave is ...:
            raw = source.read_bytes(placed.path)
            if raw is None:
                mix.warnings.append(f"sound {placed.path} not found")
                wave = None
            else:
                try:
                    wave = parse_wav(raw, placed.path)
                except ValueError as exc:
                    mix.warnings.append(str(exc))
                    wave = None
            cache[placed.path] = wave
        if wave is None:
            continue
        _add(accum, mix, wave, placed)
    limit = 32767
    mix.samples = array("h", (max(-limit, min(limit, v)) for v in accum))
    return mix


def _add(accum: List[int], mix: Mix, wave: Wave, placed: PlacedSound) -> None:
    """Add one placed sound into the accumulation, resampling and panning to stereo.

    Sequence time t inside the clip maps to the sound's own time
    (t - start) * scale + offset, so the sound's frame is that times its rate."""
    rate = mix.rate
    clip_first = max(placed.start.ticks, mix.start.ticks)
    clip_last = min(placed.start.ticks + placed.duration.ticks, mix.start.ticks + round(mix.frames / rate * Time.PER_SECOND))
    if clip_last <= clip_first:
        return
    first = round((clip_first - mix.start.ticks) / Time.PER_SECOND * rate)
    last = min(mix.frames, round((clip_last - mix.start.ticks) / Time.PER_SECOND * rate))
    if last <= first:
        return
    gain = placed.volume
    channels = wave.channels
    samples = wave.samples
    src_frames = len(samples) // channels
    # the sound's frame for the first mix frame, and the step per mix frame
    own_start = (clip_first - placed.start.ticks) / Time.PER_SECOND * placed.scale + placed.offset.ticks / Time.PER_SECOND
    step = wave.rate / rate * placed.scale
    position = own_start * wave.rate
    left, right = (0, 1) if channels >= 2 else (0, 0)
    if abs(step - 1.0) < 1e-9 and abs(position - round(position)) < 1e-6 and gain == 1.0:
        # the common case: same rate, no stretch, whole frames: straight copies
        src = int(round(position))
        count = min(last - first, src_frames - src)
        if count <= 0:
            return
        if channels >= 2:
            chunk = samples[src * 2:(src + count) * 2]
            for i, v in enumerate(chunk):
                accum[(first * 2) + i] += v
        else:
            chunk = samples[src:src + count]
            base = first * 2
            for i, v in enumerate(chunk):
                accum[base + 2 * i] += v
                accum[base + 2 * i + 1] += v
        return
    for frame in range(first, last):
        p = position + (frame - first) * step
        i = int(p)
        if i < 0 or i + 1 >= src_frames:
            continue
        t = p - i
        l = samples[i * channels + left] * (1.0 - t) + samples[(i + 1) * channels + left] * t
        r = samples[i * channels + right] * (1.0 - t) + samples[(i + 1) * channels + right] * t
        accum[frame * 2] += int(l * gain)
        accum[frame * 2 + 1] += int(r * gain)
