"""
Bounds-checked reading of Valve's binary formats.

Every Source file is a header full of `count` / `offset` pairs pointing at other
structures, and the offsets are usually relative to the struct they were read
from rather than to the file. Content can be malformed, truncated by a failed
download or compiled by a tool we have never seen, so a reader that trusts those
numbers turns a bad model into a crashed editor.

    r = Reader(data, "scout.mdl")
    count, offset = r.i32_at(156), r.i32_at(160)
    for bone in r.array(offset, count, 216):
        name = r.string_at(bone.start + bone.i32(0))

Everything raises :class:`FormatError` with the file name and what was expected,
so the caller can report "this model is broken" instead of a traceback.
"""
from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Iterator, List, Sequence, Tuple

__all__ = ["FormatError", "Reader", "Cursor"]


class FormatError(ValueError):
    """A file is not what it claims to be, or points outside itself."""


_I32 = struct.Struct("<i")
_U32 = struct.Struct("<I")
_I16 = struct.Struct("<h")
_U16 = struct.Struct("<H")
_F32 = struct.Struct("<f")
_VEC3 = struct.Struct("<3f")
_VEC4 = struct.Struct("<4f")


class Reader:
    """A byte buffer that refuses to read past its own end."""

    __slots__ = ("data", "name", "size")

    def __init__(self, data: bytes, name: str = "<memory>") -> None:
        self.data = data
        self.name = name
        self.size = len(data)

    # -- guards ------------------------------------------------------------
    def check(self, offset: int, length: int, what: str = "data") -> None:
        """Raise FormatError when the span lies outside the data."""
        if offset < 0 or length < 0 or offset + length > self.size:
            raise FormatError(
                f"{self.name}: {what} at {offset}+{length} lies outside the file ({self.size} bytes)")

    # -- scalars -----------------------------------------------------------
    def i32_at(self, offset: int) -> int:
        """Little-endian int32 at `offset`."""
        self.check(offset, 4, "int32")
        return _I32.unpack_from(self.data, offset)[0]

    def u32_at(self, offset: int) -> int:
        """Little-endian uint32 at `offset`."""
        self.check(offset, 4, "uint32")
        return _U32.unpack_from(self.data, offset)[0]

    def i16_at(self, offset: int) -> int:
        """Little-endian int16 at `offset`."""
        self.check(offset, 2, "int16")
        return _I16.unpack_from(self.data, offset)[0]

    def u16_at(self, offset: int) -> int:
        """Little-endian uint16 at `offset`."""
        self.check(offset, 2, "uint16")
        return _U16.unpack_from(self.data, offset)[0]

    def u8_at(self, offset: int) -> int:
        """Byte at `offset`."""
        self.check(offset, 1, "byte")
        return self.data[offset]

    def f32_at(self, offset: int) -> float:
        """Little-endian float at `offset`."""
        self.check(offset, 4, "float")
        return _F32.unpack_from(self.data, offset)[0]

    def vec3_at(self, offset: int) -> Tuple[float, float, float]:
        """Three floats at `offset`."""
        self.check(offset, 12, "vector")
        return _VEC3.unpack_from(self.data, offset)

    def vec4_at(self, offset: int) -> Tuple[float, float, float, float]:
        """Four floats at `offset`."""
        self.check(offset, 16, "quaternion")
        return _VEC4.unpack_from(self.data, offset)

    # -- text --------------------------------------------------------------
    def string_at(self, offset: int, limit: int = 1024) -> str:
        """A NUL-terminated string.  Valve writes these in mixed encodings."""
        if offset <= 0 or offset >= self.size:
            return ""
        end = self.data.find(b"\0", offset, min(offset + limit, self.size))
        if end < 0:
            end = min(offset + limit, self.size)
        return self.data[offset:end].decode("utf-8", "replace")

    def fixed_string_at(self, offset: int, length: int) -> str:
        """A fixed-width char[] field, trimmed at its first NUL."""
        self.check(offset, length, "string")
        raw = self.data[offset:offset + length]
        end = raw.find(b"\0")
        if end >= 0:
            raw = raw[:end]
        return raw.decode("utf-8", "replace")

    # -- bulk --------------------------------------------------------------
    def unpack_at(self, fmt: struct.Struct, offset: int, what: str = "struct"):
        """Unpack a struct at `offset` with a bounds check."""
        self.check(offset, fmt.size, what)
        return fmt.unpack_from(self.data, offset)

    def iter_structs(self, fmt: struct.Struct, offset: int, count: int, stride: int = 0,
                     what: str = "array") -> Iterator[Sequence]:
        """Walk `count` records of `fmt`, `stride` bytes apart (default: packed)."""
        step = stride or fmt.size
        if count < 0:
            raise FormatError(f"{self.name}: negative {what} count ({count})")
        self.check(offset, step * count, what)
        data = self.data
        for i in range(count):
            yield fmt.unpack_from(data, offset + i * step)

    def array(self, offset: int, count: int, stride: int, what: str = "array") -> List["Cursor"]:
        """Cursors over `count` fixed-size records - the shape of every Valve table."""
        if count < 0:
            raise FormatError(f"{self.name}: negative {what} count ({count})")
        self.check(offset, stride * count, what)
        return [Cursor(self, offset + i * stride) for i in range(count)]

    def cursor(self, offset: int) -> "Cursor":
        """A cursor whose offsets are relative to `offset`."""
        return Cursor(self, offset)

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return f"<Reader {self.name} {self.size} bytes>"


@dataclass(frozen=True)
class Cursor:
    """One record. Its fields are read at offsets relative to `start`.

    Valve's tables store offsets relative to the record itself, so keeping the
    record's own position is what makes the rest of the parsing readable.
    """

    reader: Reader
    start: int

    def i32(self, rel: int) -> int:
        """int32 at `rel` from the cursor."""
        return self.reader.i32_at(self.start + rel)

    def u32(self, rel: int) -> int:
        """uint32 at `rel` from the cursor."""
        return self.reader.u32_at(self.start + rel)

    def i16(self, rel: int) -> int:
        """int16 at `rel` from the cursor."""
        return self.reader.i16_at(self.start + rel)

    def u16(self, rel: int) -> int:
        """uint16 at `rel` from the cursor."""
        return self.reader.u16_at(self.start + rel)

    def u8(self, rel: int) -> int:
        """Byte at `rel` from the cursor."""
        return self.reader.u8_at(self.start + rel)

    def f32(self, rel: int) -> float:
        """float at `rel` from the cursor."""
        return self.reader.f32_at(self.start + rel)

    def vec3(self, rel: int) -> Tuple[float, float, float]:
        """Three floats at `rel` from the cursor."""
        return self.reader.vec3_at(self.start + rel)

    def vec4(self, rel: int) -> Tuple[float, float, float, float]:
        """Four floats at `rel` from the cursor."""
        return self.reader.vec4_at(self.start + rel)

    def string(self, rel: int) -> str:
        """Follow a `sznameindex` field: an offset relative to this record."""
        return self.reader.string_at(self.start + self.i32(rel))

    def fixed_string(self, rel: int, length: int) -> str:
        """NUL-padded string of `length` bytes at `rel`."""
        return self.reader.fixed_string_at(self.start + rel, length)

    def at(self, rel: int) -> "Cursor":
        """A nested record whose offset is stored relative to this one."""
        return Cursor(self.reader, self.start + self.i32(rel))

    def sub(self, rel: int) -> "Cursor":
        """A record at a fixed distance from this one."""
        return Cursor(self.reader, self.start + rel)
