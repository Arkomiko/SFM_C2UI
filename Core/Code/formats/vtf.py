"""
The .vtf file: Source's texture format.

A VTF holds one image at several sizes, plus optional frames and cube faces.
Two details decide how it is read:

* **mipmaps are stored smallest first**, so the full-size image is at the *end*
  of the data, and finding it means summing the sizes of everything before it;
* most textures are DXT compressed, which the GPU understands directly - so the
  raw blocks are kept as they are, and decoding to RGBA happens only when
  something needs pixels on the CPU, such as a thumbnail.

    tex = parse_vtf(data, "brick.vtf")
    tex.width, tex.height, tex.format_name
    rgba = tex.to_rgba()              # largest mip, decoded
    small = tex.to_rgba(max_size=64)  # a mip that is already small enough
"""
from __future__ import annotations

import struct
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .binary import FormatError, Reader

__all__ = ["VtfFile", "parse_vtf", "ImageFormat", "FORMAT_NAMES", "VTF_MAGIC"]

VTF_MAGIC = b"VTF\0"

# ---------------------------------------------------------------------------
#  Image formats
# ---------------------------------------------------------------------------
class ImageFormat:
    NONE = -1
    RGBA8888 = 0
    ABGR8888 = 1
    RGB888 = 2
    BGR888 = 3
    RGB565 = 4
    I8 = 5
    IA88 = 6
    P8 = 7
    A8 = 8
    RGB888_BLUESCREEN = 9
    BGR888_BLUESCREEN = 10
    ARGB8888 = 11
    BGRA8888 = 12
    DXT1 = 13
    DXT3 = 14
    DXT5 = 15
    BGRX8888 = 16
    BGR565 = 17
    BGRX5551 = 18
    BGRA4444 = 19
    DXT1_ONEBITALPHA = 20
    BGRA5551 = 21
    UV88 = 22
    UVWQ8888 = 23
    RGBA16161616F = 24
    RGBA16161616 = 25
    UVLX8888 = 26


FORMAT_NAMES: Dict[int, str] = {
    getattr(ImageFormat, n): n for n in dir(ImageFormat) if not n.startswith("_")
}

#: bits per pixel for uncompressed formats; block formats are handled separately
_BITS: Dict[int, int] = {
    ImageFormat.RGBA8888: 32, ImageFormat.ABGR8888: 32, ImageFormat.ARGB8888: 32,
    ImageFormat.BGRA8888: 32, ImageFormat.BGRX8888: 32, ImageFormat.UVWQ8888: 32,
    ImageFormat.UVLX8888: 32,
    ImageFormat.RGB888: 24, ImageFormat.BGR888: 24,
    ImageFormat.RGB888_BLUESCREEN: 24, ImageFormat.BGR888_BLUESCREEN: 24,
    ImageFormat.RGB565: 16, ImageFormat.BGR565: 16, ImageFormat.BGRX5551: 16,
    ImageFormat.BGRA4444: 16, ImageFormat.BGRA5551: 16, ImageFormat.IA88: 16,
    ImageFormat.UV88: 16,
    ImageFormat.I8: 8, ImageFormat.A8: 8, ImageFormat.P8: 8,
    ImageFormat.RGBA16161616F: 64, ImageFormat.RGBA16161616: 64,
}

_BLOCK8 = frozenset({ImageFormat.DXT1, ImageFormat.DXT1_ONEBITALPHA})
_BLOCK16 = frozenset({ImageFormat.DXT3, ImageFormat.DXT5})

# header offsets (the VTF header is packed, not naturally aligned)
_H_VERSION_MAJOR = 4
_H_VERSION_MINOR = 8
_H_HEADER_SIZE = 12
_H_WIDTH = 16
_H_HEIGHT = 18
_H_FLAGS = 20
_H_FRAMES = 24
_H_REFLECTIVITY = 32
_H_HIGH_FORMAT = 52
_H_MIP_COUNT = 56
_H_LOW_FORMAT = 57
_H_LOW_WIDTH = 61
_H_LOW_HEIGHT = 62
_H_DEPTH = 63
_H_NUM_RESOURCES = 68

_FLAG_ENVMAP = 0x4000
#: resource tag for the high-resolution image in 7.3+ files
_TAG_HIGH_RES = b"\x30\x00\x00"


def image_size(fmt: int, width: int, height: int) -> int:
    """Bytes one image of this size occupies."""
    width = max(1, width)
    height = max(1, height)
    if fmt in _BLOCK8:
        return max(1, (width + 3) // 4) * max(1, (height + 3) // 4) * 8
    if fmt in _BLOCK16:
        return max(1, (width + 3) // 4) * max(1, (height + 3) // 4) * 16
    bits = _BITS.get(fmt)
    if bits is None:
        raise FormatError(f"unsupported image format {FORMAT_NAMES.get(fmt, fmt)}")
    return width * height * bits // 8


@dataclass
class VtfFile:
    """A parsed texture.  Pixel data stays in its stored format until decoded."""

    width: int = 0
    height: int = 0
    depth: int = 1
    frames: int = 1
    flags: int = 0
    version: Tuple[int, int] = (7, 0)
    image_format: int = ImageFormat.NONE
    mip_count: int = 1
    reflectivity: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    #: mip 0 is the full-size image; raw bytes in `image_format`
    mips: List[bytes] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def format_name(self) -> str:
        return FORMAT_NAMES.get(self.image_format, str(self.image_format))

    @property
    def is_cubemap(self) -> bool:
        return bool(self.flags & _FLAG_ENVMAP)

    def mip_size(self, level: int) -> Tuple[int, int]:
        return max(1, self.width >> level), max(1, self.height >> level)

    def to_rgba(self, level: int = 0, max_size: Optional[int] = None) -> Tuple[bytes, int, int]:
        """Decode one mip to RGBA8888.

        With `max_size`, picks the smallest stored mip that is still at least
        that big - decoding a 64 px preview from a 2048 px texture should not
        cost 4 million pixels of work.
        """
        if not self.mips:
            raise FormatError("this texture has no image data")
        if max_size:
            level = 0
            for candidate in range(len(self.mips)):
                w, h = self.mip_size(candidate)
                if max(w, h) <= max_size:
                    level = candidate
                    break
                level = candidate
        level = max(0, min(level, len(self.mips) - 1))
        width, height = self.mip_size(level)
        return decode_to_rgba(self.mips[level], self.image_format, width, height), width, height


def parse_vtf(data: bytes, name: str = "texture.vtf", want_mips: bool = True) -> VtfFile:
    """Read a .vtf.  Raises :class:`FormatError` when it is not one."""
    reader = Reader(data, name)
    if reader.size < 64:
        raise FormatError(f"{name}: too small to be a texture ({reader.size} bytes)")
    if data[:4] != VTF_MAGIC:
        raise FormatError(f"{name}: not a Source texture (magic {data[:4]!r})")

    major = reader.u32_at(_H_VERSION_MAJOR)
    minor = reader.u32_at(_H_VERSION_MINOR)
    if major != 7 or minor > 6:
        raise FormatError(f"{name}: texture version {major}.{minor} is not supported")

    out = VtfFile(
        width=reader.u16_at(_H_WIDTH),
        height=reader.u16_at(_H_HEIGHT),
        flags=reader.u32_at(_H_FLAGS),
        frames=max(1, reader.u16_at(_H_FRAMES)),
        version=(major, minor),
        image_format=reader.i32_at(_H_HIGH_FORMAT),
        mip_count=max(1, reader.u8_at(_H_MIP_COUNT)),
        reflectivity=reader.vec3_at(_H_REFLECTIVITY),
    )
    if minor >= 2:
        out.depth = max(1, reader.u16_at(_H_DEPTH))
    if out.width <= 0 or out.height <= 0:
        raise FormatError(f"{name}: texture is {out.width}x{out.height}")
    if out.image_format not in _BITS and out.image_format not in _BLOCK8 \
            and out.image_format not in _BLOCK16:
        raise FormatError(f"{name}: unsupported image format "
                          f"{FORMAT_NAMES.get(out.image_format, out.image_format)}")

    start = _image_start(reader, out, minor)
    faces = 6 if out.is_cubemap else 1
    if out.is_cubemap and minor < 5:
        faces = 7                    # 7.1-7.4 cubemaps carry a spheremap face too

    _read_mips(reader, out, start, faces, want_mips)
    return out


def _image_start(reader: Reader, vtf: VtfFile, minor: int) -> int:
    """Where the high-resolution image begins."""
    header_size = reader.u32_at(_H_HEADER_SIZE)

    if minor >= 3:
        # 7.3+ keeps a resource table; the high-res image has its own entry
        count = reader.u32_at(_H_NUM_RESOURCES)
        if 0 < count <= 64:
            base = 80
            for i in range(count):
                entry = base + i * 8
                if entry + 8 > reader.size:
                    break
                tag = reader.data[entry:entry + 3]
                offset = reader.u32_at(entry + 4)
                if tag == _TAG_HIGH_RES:
                    return offset
        vtf.warnings.append("no high-resolution image resource; falling back to the header size")
        return header_size

    # before 7.3 the low-resolution thumbnail sits between header and image
    low_format = reader.i32_at(_H_LOW_FORMAT)
    low_w = reader.u8_at(_H_LOW_WIDTH)
    low_h = reader.u8_at(_H_LOW_HEIGHT)
    start = header_size
    if low_format >= 0 and low_w and low_h:
        try:
            start += image_size(low_format, low_w, low_h)
        except FormatError:
            vtf.warnings.append("thumbnail is in an unknown format; image offset may be wrong")
    return start


def _read_mips(reader: Reader, vtf: VtfFile, start: int, faces: int, want_mips: bool) -> None:
    """Slice out the mip levels.

    Stored order is smallest mip first, and within a mip: every frame, then
    every face. Only the first frame and face are kept - animated textures and
    cubemaps are not something the editor draws yet.
    """
    fmt = vtf.image_format
    levels = vtf.mip_count
    sizes = []
    for level in range(levels):
        w, h = vtf.mip_size(level)
        try:
            sizes.append(image_size(fmt, w, h))
        except FormatError as exc:
            vtf.warnings.append(str(exc))
            return

    offset = start
    found: Dict[int, bytes] = {}
    slices = vtf.frames * faces * max(1, vtf.depth)
    for level in reversed(range(levels)):          # smallest first on disk
        per_slice = sizes[level]
        block = per_slice * slices
        if offset + per_slice > reader.size:
            vtf.warnings.append(
                f"image data ends early: mip {level} needs {per_slice} bytes at {offset}, "
                f"file is {reader.size}")
            break
        found[level] = reader.data[offset:offset + per_slice]     # first frame, first face
        offset += block
        if not want_mips and level == 0:
            break

    if not found:
        vtf.warnings.append("no usable image data")
        vtf.mips = []
        return
    vtf.mips = [found[level] for level in sorted(found)]
    if 0 not in found:
        vtf.warnings.append("the full-size image is missing; using the largest one present")
        vtf.width, vtf.height = vtf.mip_size(min(found))


# ---------------------------------------------------------------------------
#  Decoding
# ---------------------------------------------------------------------------
def decode_to_rgba(data: bytes, fmt: int, width: int, height: int) -> bytes:
    """Turn stored pixels into RGBA8888."""
    if fmt in _BLOCK8 or fmt in _BLOCK16:
        return _decode_dxt(data, fmt, width, height)
    return _decode_plain(data, fmt, width, height)


def _decode_plain(data: bytes, fmt: int, width: int, height: int) -> bytes:
    count = width * height
    out = bytearray(count * 4)

    if fmt == ImageFormat.RGBA8888:
        return bytes(data[:count * 4].ljust(count * 4, b"\0"))
    if fmt in (ImageFormat.BGRA8888, ImageFormat.BGRX8888):
        for i in range(count):
            b, g, r, a = data[i * 4:i * 4 + 4]
            j = i * 4
            out[j] = r; out[j + 1] = g; out[j + 2] = b
            out[j + 3] = 255 if fmt == ImageFormat.BGRX8888 else a
        return bytes(out)
    if fmt == ImageFormat.ABGR8888:
        for i in range(count):
            a, b, g, r = data[i * 4:i * 4 + 4]
            j = i * 4
            out[j] = r; out[j + 1] = g; out[j + 2] = b; out[j + 3] = a
        return bytes(out)
    if fmt == ImageFormat.ARGB8888:
        for i in range(count):
            a, r, g, b = data[i * 4:i * 4 + 4]
            j = i * 4
            out[j] = r; out[j + 1] = g; out[j + 2] = b; out[j + 3] = a
        return bytes(out)
    if fmt in (ImageFormat.RGB888, ImageFormat.RGB888_BLUESCREEN):
        for i in range(count):
            r, g, b = data[i * 3:i * 3 + 3]
            j = i * 4
            out[j] = r; out[j + 1] = g; out[j + 2] = b; out[j + 3] = 255
        return bytes(out)
    if fmt in (ImageFormat.BGR888, ImageFormat.BGR888_BLUESCREEN):
        for i in range(count):
            b, g, r = data[i * 3:i * 3 + 3]
            j = i * 4
            out[j] = r; out[j + 1] = g; out[j + 2] = b; out[j + 3] = 255
        return bytes(out)
    if fmt in (ImageFormat.RGB565, ImageFormat.BGR565):
        swap = fmt == ImageFormat.BGR565
        for i in range(count):
            value = data[i * 2] | (data[i * 2 + 1] << 8)
            r = ((value >> 11) & 0x1F) * 255 // 31
            g = ((value >> 5) & 0x3F) * 255 // 63
            b = (value & 0x1F) * 255 // 31
            j = i * 4
            if swap:
                r, b = b, r
            out[j] = r; out[j + 1] = g; out[j + 2] = b; out[j + 3] = 255
        return bytes(out)
    if fmt == ImageFormat.I8:
        for i in range(count):
            v = data[i]
            j = i * 4
            out[j] = out[j + 1] = out[j + 2] = v
            out[j + 3] = 255
        return bytes(out)
    if fmt == ImageFormat.A8:
        for i in range(count):
            j = i * 4
            out[j] = out[j + 1] = out[j + 2] = 255
            out[j + 3] = data[i]
        return bytes(out)
    if fmt == ImageFormat.IA88:
        for i in range(count):
            v, a = data[i * 2], data[i * 2 + 1]
            j = i * 4
            out[j] = out[j + 1] = out[j + 2] = v
            out[j + 3] = a
        return bytes(out)
    if fmt == ImageFormat.BGRA4444:
        for i in range(count):
            value = data[i * 2] | (data[i * 2 + 1] << 8)
            b = (value & 0xF) * 17
            g = ((value >> 4) & 0xF) * 17
            r = ((value >> 8) & 0xF) * 17
            a = ((value >> 12) & 0xF) * 17
            j = i * 4
            out[j] = r; out[j + 1] = g; out[j + 2] = b; out[j + 3] = a
        return bytes(out)
    if fmt in (ImageFormat.BGRA5551, ImageFormat.BGRX5551):
        for i in range(count):
            value = data[i * 2] | (data[i * 2 + 1] << 8)
            b = (value & 0x1F) * 255 // 31
            g = ((value >> 5) & 0x1F) * 255 // 31
            r = ((value >> 10) & 0x1F) * 255 // 31
            a = 255 if fmt == ImageFormat.BGRX5551 or (value & 0x8000) else 0
            j = i * 4
            out[j] = r; out[j + 1] = g; out[j + 2] = b; out[j + 3] = a
        return bytes(out)

    if fmt == ImageFormat.UV88:
        # a two-channel normal map: keep R and G, fill the rest
        for i in range(count):
            j = i * 4
            out[j] = data[i * 2]; out[j + 1] = data[i * 2 + 1]
            out[j + 2] = 128; out[j + 3] = 255
        return bytes(out)
    if fmt == ImageFormat.RGBA16161616:
        for i in range(count):
            j = i * 4
            k = i * 8
            out[j] = data[k + 1]; out[j + 1] = data[k + 3]
            out[j + 2] = data[k + 5]; out[j + 3] = data[k + 7]
        return bytes(out)
    if fmt == ImageFormat.RGBA16161616F:
        # HDR: half floats, clamped to 0..1 - a tone mapper belongs in the renderer
        values = struct.unpack_from(f"<{count * 4}e", data)
        for i, v in enumerate(values):
            out[i] = 255 if v >= 1.0 else 0 if v <= 0.0 or v != v else int(v * 255 + 0.5)
        return bytes(out)

    raise FormatError(f"cannot decode image format {FORMAT_NAMES.get(fmt, fmt)}")


def _decode_dxt(data: bytes, fmt: int, width: int, height: int) -> bytes:
    """Expand DXT1/3/5 blocks to RGBA8888."""
    blocks_x = max(1, (width + 3) // 4)
    blocks_y = max(1, (height + 3) // 4)
    stride = width * 4
    out = bytearray(width * height * 4)
    block_bytes = 8 if fmt in _BLOCK8 else 16
    has_alpha_block = fmt in _BLOCK16
    dxt5 = fmt == ImageFormat.DXT5
    unpack_u16 = struct.Struct("<H").unpack_from
    unpack_u32 = struct.Struct("<I").unpack_from

    for by in range(blocks_y):
        for bx in range(blocks_x):
            offset = (by * blocks_x + bx) * block_bytes
            if offset + block_bytes > len(data):
                break

            alpha = None
            colour_offset = offset
            if has_alpha_block:
                colour_offset = offset + 8
                if dxt5:
                    a0 = data[offset]
                    a1 = data[offset + 1]
                    table = [a0, a1]
                    if a0 > a1:
                        for i in range(1, 7):
                            table.append(((7 - i) * a0 + i * a1) // 7)
                    else:
                        for i in range(1, 5):
                            table.append(((5 - i) * a0 + i * a1) // 5)
                        table.append(0)
                        table.append(255)
                    bits = int.from_bytes(data[offset + 2:offset + 8], "little")
                    alpha = [table[(bits >> (3 * i)) & 0x7] for i in range(16)]
                else:
                    raw = data[offset:offset + 8]
                    alpha = []
                    for i in range(8):
                        value = raw[i]
                        alpha.append((value & 0xF) * 17)
                        alpha.append((value >> 4) * 17)

            c0 = unpack_u16(data, colour_offset)[0]
            c1 = unpack_u16(data, colour_offset + 2)[0]
            bits = unpack_u32(data, colour_offset + 4)[0]

            r0 = ((c0 >> 11) & 0x1F) * 255 // 31
            g0 = ((c0 >> 5) & 0x3F) * 255 // 63
            b0 = (c0 & 0x1F) * 255 // 31
            r1 = ((c1 >> 11) & 0x1F) * 255 // 31
            g1 = ((c1 >> 5) & 0x3F) * 255 // 63
            b1 = (c1 & 0x1F) * 255 // 31

            if c0 > c1 or has_alpha_block:
                colours = (
                    (r0, g0, b0, 255), (r1, g1, b1, 255),
                    ((2 * r0 + r1) // 3, (2 * g0 + g1) // 3, (2 * b0 + b1) // 3, 255),
                    ((r0 + 2 * r1) // 3, (g0 + 2 * g1) // 3, (b0 + 2 * b1) // 3, 255),
                )
            else:
                # one-bit alpha: the fourth entry is transparent black
                colours = (
                    (r0, g0, b0, 255), (r1, g1, b1, 255),
                    ((r0 + r1) // 2, (g0 + g1) // 2, (b0 + b1) // 2, 255),
                    (0, 0, 0, 0),
                )

            for py in range(4):
                y = by * 4 + py
                if y >= height:
                    break
                row = y * stride
                for px in range(4):
                    x = bx * 4 + px
                    if x >= width:
                        break
                    index = py * 4 + px
                    r, g, b, a = colours[(bits >> (2 * index)) & 0x3]
                    if alpha is not None:
                        a = alpha[index]
                    j = row + x * 4
                    out[j] = r; out[j + 1] = g; out[j + 2] = b; out[j + 3] = a
    return bytes(out)
