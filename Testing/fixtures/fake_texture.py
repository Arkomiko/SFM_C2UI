"""
Build a Source texture in memory, byte for byte.

    data = build_vtf(pixels, width, height, fmt=ImageFormat.BGR888)

`pixels` is a flat list of RGBA tuples, top row first. Uncompressed formats are
packed from it directly; DXT formats encode each 4x4 block with two colours and
per-pixel indices, which is enough to test the decoder against known values.

Mips are written the way the engine writes them: smallest first. Versions 7.2
(header + thumbnail + image) and 7.3+ (header + resource table) are both
supported so the two ways of locating the image are both covered.
"""
from __future__ import annotations

import struct
from typing import List, Optional, Sequence, Tuple

from Core.Code.formats.vtf import ImageFormat, image_size

__all__ = ["build_vtf", "encode_pixels", "RGBA", "FLAG_ENVMAP"]

RGBA = Tuple[int, int, int, int]
FLAG_ENVMAP = 0x4000


def _rgb565(r: int, g: int, b: int) -> int:
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)


def _block_pixels(pixels: Sequence[RGBA], width: int, height: int, bx: int, by: int) -> List[RGBA]:
    out = []
    for py in range(4):
        for px in range(4):
            x, y = min(bx * 4 + px, width - 1), min(by * 4 + py, height - 1)
            out.append(pixels[y * width + x])
    return out


def _encode_dxt1_block(block: List[RGBA]) -> bytes:
    """Two colours - the first two distinct ones in the block - with each pixel
    snapped to whichever is nearer. c0 > c1 keeps the four-colour mode."""
    distinct = []
    for p in block:
        c = _rgb565(*p[:3])
        if c not in distinct:
            distinct.append(c)
    c0 = max(distinct)
    c1 = min(distinct) if len(distinct) > 1 else 0
    indices = 0
    for i, p in enumerate(block):
        c = _rgb565(*p[:3])
        indices |= (0 if c == c0 or abs(c - c0) <= abs(c - c1) else 1) << (2 * i)
    return struct.pack("<HHI", c0, c1, indices)


def _encode_dxt5_alpha(block: List[RGBA]) -> bytes:
    """Alpha via the 8-entry table with a0 > a1, indices chosen exactly for
    a0 and a1 and by nearest value otherwise."""
    alphas = sorted({p[3] for p in block}, reverse=True)
    a0 = alphas[0]
    a1 = alphas[-1] if len(alphas) > 1 else max(0, a0 - 1)
    if a0 == a1:
        a0, a1 = (255, 254) if a0 == 255 else (a0 + 1, a0)
    table = [a0, a1] + [((7 - i) * a0 + i * a1) // 7 for i in range(1, 7)]
    bits = 0
    for i, p in enumerate(block):
        best = min(range(8), key=lambda k: abs(table[k] - p[3]))
        bits |= best << (3 * i)
    return bytes([a0, a1]) + bits.to_bytes(6, "little")


def encode_pixels(pixels: Sequence[RGBA], width: int, height: int, fmt: int) -> bytes:
    if fmt in (ImageFormat.DXT1, ImageFormat.DXT5):
        out = bytearray()
        for by in range(max(1, (height + 3) // 4)):
            for bx in range(max(1, (width + 3) // 4)):
                block = _block_pixels(pixels, width, height, bx, by)
                if fmt == ImageFormat.DXT5:
                    out += _encode_dxt5_alpha(block)
                out += _encode_dxt1_block(block)
        return bytes(out)
    out = bytearray()
    for r, g, b, a in pixels:
        if fmt == ImageFormat.RGBA8888:
            out += bytes((r, g, b, a))
        elif fmt == ImageFormat.BGRA8888:
            out += bytes((b, g, r, a))
        elif fmt == ImageFormat.ABGR8888:
            out += bytes((a, b, g, r))
        elif fmt == ImageFormat.ARGB8888:
            out += bytes((a, r, g, b))
        elif fmt == ImageFormat.BGR888:
            out += bytes((b, g, r))
        elif fmt == ImageFormat.RGB888:
            out += bytes((r, g, b))
        elif fmt == ImageFormat.I8:
            out += bytes((r,))
        elif fmt == ImageFormat.A8:
            out += bytes((a,))
        elif fmt == ImageFormat.IA88:
            out += bytes((r, a))
        elif fmt == ImageFormat.UV88:
            out += bytes((r, g))
        elif fmt == ImageFormat.BGRA4444:
            out += struct.pack("<H", (a >> 4) << 12 | (r >> 4) << 8 | (g >> 4) << 4 | (b >> 4))
        elif fmt == ImageFormat.RGBA16161616F:
            out += struct.pack("<4e", r / 255, g / 255, b / 255, a / 255)
        else:
            raise ValueError(f"fixture cannot encode format {fmt}")
    return bytes(out)


def _mip_pixels(pixels: Sequence[RGBA], width: int, height: int, level: int) -> Tuple[List[RGBA], int, int]:
    """Point-sample a smaller level; exact enough for a fixture."""
    w, h = max(1, width >> level), max(1, height >> level)
    out = []
    for y in range(h):
        for x in range(w):
            out.append(pixels[(y << level) * width + (x << level)])
    return out, w, h


def build_vtf(pixels: Sequence[RGBA], width: int, height: int,
              fmt: int = ImageFormat.RGBA8888, version: Tuple[int, int] = (7, 2),
              mips: int = 1, frames: int = 1, flags: int = 0,
              thumbnail: bool = True, faces: Optional[int] = None,
              truncate: int = 0) -> bytes:
    """Assemble a .vtf.

    `mips` levels are written smallest first. With `thumbnail`, a 7.2 file
    carries a 4x4 DXT1 low-res image between header and data - which is what
    shipped files do, and what a reader gets wrong if it ignores it.
    `faces` writes that many copies per mip (a cubemap). `truncate` chops
    bytes off the end to test the reader's handling of short files.
    """
    major, minor = version
    faces = faces or 1
    thumb_fmt = ImageFormat.DXT1 if thumbnail and minor < 3 else -1
    thumb = bytes(8) if thumb_fmt >= 0 else b""

    # 7.2 files ship with an 80-byte header; 7.3+ put the resource table at 80.
    # The value is deliberately generous so a reader that assumes a fixed size
    # instead of honouring the field reads the wrong bytes.
    header_size = 96
    head = bytearray()
    head += b"VTF\0"
    head += struct.pack("<II", major, minor)
    head += struct.pack("<I", header_size)
    head += struct.pack("<HH", width, height)
    head += struct.pack("<I", flags)
    head += struct.pack("<HH", frames, 0)
    head += bytes(4)
    head += struct.pack("<3f", 0.5, 0.5, 0.5)
    head += bytes(4)
    head += struct.pack("<f", 1.0)
    head += struct.pack("<i", fmt)
    head += struct.pack("<B", mips)
    head += struct.pack("<i", thumb_fmt)
    head += struct.pack("<BB", 4 if thumb else 0, 4 if thumb else 0)
    head += struct.pack("<H", 1)                      # depth (7.2+)
    if minor >= 3:
        head += bytes(3)
        head += struct.pack("<I", 1)                  # numResources
        head += bytes(80 - len(head))
        head += b"\x30\x00\x00" + b"\x00" + struct.pack("<I", header_size)
    head += bytes(header_size - len(head))
    assert len(head) == header_size, (len(head), header_size)

    body = bytearray()
    for level in reversed(range(mips)):
        px, w, h = _mip_pixels(pixels, width, height, level)
        encoded = encode_pixels(px, w, h, fmt)
        assert len(encoded) == image_size(fmt, w, h), (level, len(encoded))
        for _frame in range(frames):
            for _face in range(faces):
                body += encoded

    data = bytes(head) + thumb + bytes(body)
    return data[:-truncate] if truncate else data
