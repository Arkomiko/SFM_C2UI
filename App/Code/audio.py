"""
Playing the sequence's sound in the editor.

The mixed track (`Core.Code.sound.mix_sequence`) is handed to the system's
default output through Qt Multimedia; playback starts at any sequence time
and reports how far it has got, so the timeline can follow the sound rather
than a clock and stay in step with it.

    player = SoundPlayer()
    player.set_mix(mix)
    player.play_from(Time.from_seconds(4))
    player.elapsed()                    # Time since play_from, as heard
    player.stop()
"""
from __future__ import annotations

import logging
from typing import Optional

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QObject
from PySide6.QtMultimedia import QAudioFormat, QAudioSink, QMediaDevices

from Core.API.dmx import Time
from Core.Code.sound import Mix

__all__ = ["SoundPlayer"]

log = logging.getLogger("c2ui.audio")


class SoundPlayer(QObject):
    """Plays a `Mix` from any point through the default audio output."""

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.mix: Optional[Mix] = None
        self._sink: Optional[QAudioSink] = None
        self._buffer: Optional[QBuffer] = None
        self._data = QByteArray()
        self._from = Time(0)
        self._playing = False
        self.volume = 1.0

    @property
    def available(self) -> bool:
        """True when there is a mix with sound in it to play."""
        return self.mix is not None and self.mix.frames > 0

    @property
    def playing(self) -> bool:
        """True between play_from and stop."""
        return self._playing

    def set_mix(self, mix: Optional[Mix]) -> None:
        """Take a new mix (or none); stops whatever plays."""
        self.stop()
        self.mix = mix
        self._data = QByteArray(mix.samples.tobytes()) if mix is not None else QByteArray()

    def play_from(self, start: Time) -> bool:
        """Start playing at `start` (sequence time); False when there is nothing to play
        or no output device."""
        self.stop()
        mix = self.mix
        if mix is None or not mix.frames:
            return False
        device = QMediaDevices.defaultAudioOutput()
        if device.isNull():
            return False
        fmt = QAudioFormat()
        fmt.setSampleRate(mix.rate)
        fmt.setChannelCount(mix.channels)
        fmt.setSampleFormat(QAudioFormat.Int16)
        if not device.isFormatSupported(fmt):
            fmt = device.preferredFormat()
            if fmt.sampleFormat() != QAudioFormat.Int16 or fmt.sampleRate() != mix.rate:
                log.warning("audio output wants %s; the mix is 16-bit at %d", fmt, mix.rate)
                return False
        frame = round((start.ticks - mix.start.ticks) / Time.PER_SECOND * mix.rate)
        offset = max(0, min(frame, mix.frames)) * mix.channels * 2
        self._buffer = QBuffer(self._data)
        self._buffer.open(QIODevice.ReadOnly)
        self._buffer.seek(offset)
        self._sink = QAudioSink(device, fmt)
        self._sink.setVolume(self.volume)
        self._sink.start(self._buffer)
        self._from = start
        self._playing = True
        return True

    def elapsed(self) -> Time:
        """How much has been heard since `play_from`."""
        if self._sink is None or not self._playing:
            return Time(0)
        return Time(round(self._sink.processedUSecs() / 1_000_000 * Time.PER_SECOND))

    def stop(self) -> None:
        """Silence."""
        self._playing = False
        if self._sink is not None:
            self._sink.stop()
            self._sink.deleteLater()
            self._sink = None
        if self._buffer is not None:
            self._buffer.close()
            self._buffer = None
