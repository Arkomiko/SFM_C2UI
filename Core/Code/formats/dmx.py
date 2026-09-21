"""
The .dmx file: Valve's Datamodel serialised.

Two encodings exist in shipped content and both are handled: **binary** in
versions 1 to 5 (sessions are binary 5, particle systems 2 to 5) and
**keyvalues2**, the text form. What changed between binary versions is only
how strings are stored:

    version   string table   element name   string values   type 7
    1         none           inline         inline          ObjectID
    2, 3      short count,   inline         inline          ObjectID (2)
              short index                                    Time (3)
    4         int count,     table          table           Time
              short index
    5         int count,     table          table           Time
              int index

String *arrays* are inline in every version. Everything else - element
headers, attribute types, arrays, vectors - is the same throughout.

Writing reproduces a file byte for byte when nothing was changed: the string
table is kept in the order it was read and elements keep their order. That is
the test the writer is held to, over every session and particle file in the
installation.

    doc = parse_dmx(data)                  # bytes -> DmxDocument
    data = serialise_dmx(doc)              # DmxDocument -> bytes
    doc = load_dmx(path); save_dmx(doc, path)
"""
from __future__ import annotations

import re
import struct
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from Core.API.dmx import (ARRAY_OFFSET, TYPE_IDS, AttrType, DmxDocument, Element, Time, is_array,
                          type_id, type_name)

from .binary import FormatError

__all__ = ["parse_dmx", "serialise_dmx", "load_dmx", "save_dmx", "read_header", "DmxHeader"]

_HEADER = re.compile(rb"<!-- dmx encoding (\w+) (\d+) format (\w+) (\d+) -->\r?\n")
_MAX_ELEMENTS = 50_000_000
_MAX_STRINGS = 50_000_000


class DmxHeader:
    """The ``<!-- dmx encoding ... -->`` line, parsed."""
    __slots__ = ("encoding", "encoding_version", "format", "format_version", "length")

    def __init__(self, encoding: str, encoding_version: int, format_: str,
                 format_version: int, length: int) -> None:
        self.encoding = encoding
        self.encoding_version = encoding_version
        self.format = format_
        self.format_version = format_version
        self.length = length


def read_header(data: bytes, name: str = "") -> DmxHeader:
    """Parse the header line; raises FormatError when absent."""
    match = _HEADER.match(data)
    if not match:
        raise FormatError(f"{name or 'dmx'}: not a DMX file (no header)")
    return DmxHeader(match.group(1).decode("ascii"), int(match.group(2)),
                     match.group(3).decode("ascii"), int(match.group(4)), match.end())


# ===========================================================================
#  Binary
# ===========================================================================
_S_INT = struct.Struct("<i")
_S_SHORT = struct.Struct("<h")
_S_FLOAT = struct.Struct("<f")
_S_COLOR = struct.Struct("<4B")
_S_VEC = {AttrType.VECTOR2: struct.Struct("<2f"), AttrType.VECTOR3: struct.Struct("<3f"),
          AttrType.VECTOR4: struct.Struct("<4f"), AttrType.QANGLE: struct.Struct("<3f"),
          AttrType.QUATERNION: struct.Struct("<4f"), AttrType.MATRIX: struct.Struct("<16f")}


class _Layout:
    """What a binary version does with strings."""

    def __init__(self, version: int) -> None:
        if not 1 <= version <= 5:
            raise FormatError(f"binary encoding version {version} is not supported")
        self.version = version
        self.has_table = version >= 2
        self.count_struct = _S_INT if version >= 4 else _S_SHORT
        self.index_struct = _S_INT if version >= 5 else _S_SHORT
        self.names_in_table = version >= 4          # element names and string values
        self.type7_is_time = version >= 3


class _BinaryReader:
    def __init__(self, data: bytes, offset: int, name: str) -> None:
        self.data = data
        self.pos = offset
        self.name = name

    def need(self, count: int, what: str) -> None:
        """Raise FormatError unless `count` bytes remain."""
        if self.pos + count > len(self.data):
            raise FormatError(f"{self.name}: truncated while reading {what} at {self.pos}")

    def unpack(self, s: struct.Struct, what: str = "value"):
        """Unpack a struct and advance."""
        self.need(s.size, what)
        value = s.unpack_from(self.data, self.pos)
        self.pos += s.size
        return value

    def int(self, what: str = "int") -> int:
        """One int32."""
        return self.unpack(_S_INT, what)[0]

    def raw(self, count: int, what: str) -> bytes:
        """`count` bytes, advancing."""
        self.need(count, what)
        out = self.data[self.pos:self.pos + count]
        self.pos += count
        return out

    def cstring(self, what: str = "string") -> str:
        """A NUL-terminated string."""
        end = self.data.find(b"\0", self.pos)
        if end < 0:
            raise FormatError(f"{self.name}: unterminated {what} at {self.pos}")
        out = self.data[self.pos:end]
        self.pos = end + 1
        return out.decode("utf-8", "surrogateescape")


def _parse_binary(data: bytes, header: DmxHeader, name: str) -> DmxDocument:
    layout = _Layout(header.encoding_version)
    r = _BinaryReader(data, header.length, name)
    r.need(1, "header terminator")
    if data[r.pos] != 0:
        raise FormatError(f"{name}: header is not NUL-terminated")
    r.pos += 1

    doc = DmxDocument(encoding="binary", encoding_version=header.encoding_version,
                      format=header.format, format_version=header.format_version)

    # string table
    if layout.has_table:
        count = r.unpack(layout.count_struct, "string count")[0]
        if count < 0 or count > _MAX_STRINGS:
            raise FormatError(f"{name}: implausible string count {count}")
        doc.strings = [r.cstring("table string") for _ in range(count)]

    def table_string(what: str) -> str:
        """A string referenced by table index."""
        index = r.unpack(layout.index_struct, what)[0]
        if not 0 <= index < len(doc.strings):
            raise FormatError(f"{name}: string index {index} out of range for {what}")
        return doc.strings[index]

    # element headers
    element_count = r.int("element count")
    if element_count < 0 or element_count > _MAX_ELEMENTS:
        raise FormatError(f"{name}: implausible element count {element_count}")
    for _ in range(element_count):
        etype = table_string("element type") if layout.has_table else r.cstring("element type")
        ename = table_string("element name") if layout.names_in_table else r.cstring("element name")
        guid = uuid.UUID(bytes_le=r.raw(16, "element id"))
        doc.add(Element(etype, ename, guid))

    # attributes
    def element_ref() -> Any:
        """An element reference: index, -1 for none, -2 for an external GUID."""
        index = r.int("element index")
        if index == -1:
            return None
        if index == -2:
            return uuid.UUID(r.cstring("external element id"))
        if not 0 <= index < element_count:
            raise FormatError(f"{name}: element index {index} out of range")
        return doc.elements[index]

    def value(kind: int) -> Any:
        """One attribute value of type `kind`."""
        if kind == AttrType.ELEMENT:
            return element_ref()
        if kind == AttrType.INT:
            return r.int()
        if kind == AttrType.FLOAT:
            return r.unpack(_S_FLOAT)[0]
        if kind == AttrType.BOOL:
            return r.raw(1, "bool") != b"\0"
        if kind == AttrType.STRING:
            return r.cstring("string value")
        if kind == AttrType.BINARY:
            length = r.int("binary length")
            if length < 0:
                raise FormatError(f"{name}: negative binary length")
            return r.raw(length, "binary value")
        if kind == AttrType.TIME:
            if layout.type7_is_time:
                return Time(r.int("time"))
            return uuid.UUID(bytes_le=r.raw(16, "object id"))
        if kind == AttrType.COLOR:
            return r.unpack(_S_COLOR)
        vec = _S_VEC.get(kind)
        if vec is not None:
            return r.unpack(vec)
        raise FormatError(f"{name}: unknown attribute type {kind} at {r.pos}")

    for element in doc.elements:
        attr_count = r.int("attribute count")
        if attr_count < 0:
            raise FormatError(f"{name}: negative attribute count")
        for _ in range(attr_count):
            aname = table_string("attribute name") if layout.has_table else r.cstring("attribute name")
            kind = r.raw(1, "attribute type")[0]
            if is_array(kind):
                base = kind - ARRAY_OFFSET
                count = r.int("array length")
                if count < 0:
                    raise FormatError(f"{name}: negative array length")
                if base == AttrType.STRING:
                    items = [r.cstring("string array item") for _ in range(count)]
                else:
                    items = [value(base) for _ in range(count)]
                element.set(aname, kind, items)
            elif kind == AttrType.STRING and layout.names_in_table:
                element.set(aname, kind, table_string("string value"))
            else:
                element.set(aname, kind, value(kind))
    return doc


class _StringTable:
    """The table to write: what was read, plus anything new, in that order."""

    def __init__(self, existing: List[str]) -> None:
        self.strings = list(existing)
        self.index: Dict[str, int] = {}
        for i, s in enumerate(self.strings):
            self.index.setdefault(s, i)

    def add(self, s: str) -> int:
        """Intern a string; returns its index."""
        i = self.index.get(s)
        if i is None:
            i = len(self.strings)
            self.strings.append(s)
            self.index[s] = i
        return i


def _serialise_binary(doc: DmxDocument) -> bytes:
    layout = _Layout(doc.encoding_version)
    out = bytearray()
    out += f"<!-- dmx encoding binary {doc.encoding_version} format {doc.format} {doc.format_version} -->\n".encode("ascii")
    out += b"\0"

    positions = {id(e): i for i, e in enumerate(doc.elements)}
    table = _StringTable(doc.strings)

    def encode(s: str) -> bytes:
        """UTF-8 with a NUL terminator, surrogates passed through."""
        return s.encode("utf-8", "surrogateescape") + b"\0"

    # pass one: collect strings in the order the reader would have met them,
    # so a file written from scratch gets a stable, sensible table too
    if layout.has_table:
        for e in doc.elements:
            table.add(e.type)
            if layout.names_in_table:
                table.add(e.name)
        for e in doc.elements:
            for a in e:
                table.add(a.name)
                if a.type == AttrType.STRING and layout.names_in_table:
                    table.add(a.value)

    body = bytearray()

    def write_string(s: str, in_table: bool) -> None:
        """A string in the table (versions that have one) or inline."""
        if in_table:
            body.extend(layout.index_struct.pack(table.add(s)))
        else:
            body.extend(encode(s))

    def element_ref(v: Any) -> None:
        """An element reference: index, -1 for none, -2 for an external GUID."""
        if v is None:
            body.extend(_S_INT.pack(-1))
        elif isinstance(v, uuid.UUID):
            body.extend(_S_INT.pack(-2))
            body.extend(encode(str(v)))
        else:
            index = positions.get(id(v))
            if index is None:
                raise FormatError(f"element {v!r} is referenced but not in the document")
            body.extend(_S_INT.pack(index))

    def write_value(kind: int, v: Any) -> None:
        """One attribute value of type `kind`."""
        if kind == AttrType.ELEMENT:
            element_ref(v)
        elif kind == AttrType.INT:
            body.extend(_S_INT.pack(int(v)))
        elif kind == AttrType.FLOAT:
            body.extend(_S_FLOAT.pack(float(v)))
        elif kind == AttrType.BOOL:
            body.append(1 if v else 0)
        elif kind == AttrType.STRING:
            body.extend(encode(v))
        elif kind == AttrType.BINARY:
            body.extend(_S_INT.pack(len(v)))
            body.extend(v)
        elif kind == AttrType.TIME:
            if layout.type7_is_time:
                body.extend(_S_INT.pack(v.ticks if isinstance(v, Time) else int(v)))
            else:
                body.extend(v.bytes_le)
        elif kind == AttrType.COLOR:
            body.extend(_S_COLOR.pack(*v))
        elif kind in _S_VEC:
            body.extend(_S_VEC[kind].pack(*v))
        else:
            raise FormatError(f"unknown attribute type {kind}")

    body.extend(_S_INT.pack(len(doc.elements)))
    for e in doc.elements:
        write_string(e.type, layout.has_table)
        write_string(e.name, layout.names_in_table)
        body.extend(e.id.bytes_le)

    for e in doc.elements:
        body.extend(_S_INT.pack(len(e)))
        for a in e:
            write_string(a.name, layout.has_table)
            body.append(a.type)
            if a.is_array:
                base = a.type - ARRAY_OFFSET
                body.extend(_S_INT.pack(len(a.value)))
                for item in a.value:
                    write_value(base, item)
            elif a.type == AttrType.STRING and layout.names_in_table:
                write_string(a.value, True)
            else:
                write_value(a.type, a.value)

    if layout.has_table:
        out += layout.count_struct.pack(len(table.strings))
        for s in table.strings:
            out += encode(s)
    out += body
    return bytes(out)


# ===========================================================================
#  KeyValues2 (text)
# ===========================================================================
_KV2_TOKEN = re.compile(r'\s*(?:"((?:[^"\\]|\\.)*)"|([{}\[\],])|//[^\n]*\n?)', re.DOTALL)


def _kv2_tokens(text: str, name: str) -> List[str]:
    tokens: List[str] = []
    pos = 0
    length = len(text)
    while pos < length:
        m = _KV2_TOKEN.match(text, pos)
        if not m or m.end() == pos:
            if text[pos:].strip() == "":
                break
            raise FormatError(f"{name}: cannot read keyvalues2 near offset {pos}")
        pos = m.end()
        if m.group(1) is not None:
            tokens.append(m.group(1).replace('\\"', '"').replace("\\\\", "\\"))
        elif m.group(2) is not None:
            tokens.append(m.group(2))
    return tokens


def _kv2_scalar(kind: int, text: str) -> Any:
    if kind == AttrType.INT:
        return int(text)
    if kind == AttrType.FLOAT:
        return float(text)
    if kind == AttrType.BOOL:
        return text.strip() not in ("0", "", "false")
    if kind == AttrType.STRING:
        return text
    if kind == AttrType.BINARY:
        return bytes.fromhex(text)
    if kind == AttrType.TIME:
        return Time.from_seconds(float(text))
    if kind == AttrType.COLOR:
        return tuple(int(v) for v in text.split())
    if kind in _S_VEC:
        return tuple(float(v) for v in text.split())
    raise FormatError(f"keyvalues2: cannot read a {type_name(kind)} from {text!r}")


def _parse_kv2(data: bytes, header: DmxHeader, name: str) -> DmxDocument:
    text = data[header.length:].decode("utf-8", "surrogateescape")
    tokens = _kv2_tokens(text, name)
    doc = DmxDocument(encoding="keyvalues2", encoding_version=header.encoding_version,
                      format=header.format, format_version=header.format_version,
                      line_ending="\r\n" if data[:header.length].endswith(b"\r\n") else "\n")
    pos = 0
    pending: List[Tuple[Element, str, int, uuid.UUID]] = []     # element refs to fix up by id

    def expect(tok: str) -> None:
        """Consume `tok` or raise FormatError."""
        nonlocal pos
        if pos >= len(tokens) or tokens[pos] != tok:
            got = tokens[pos] if pos < len(tokens) else "<end>"
            raise FormatError(f"{name}: expected {tok!r}, got {got!r}")
        pos += 1

    def next_token(what: str) -> str:
        """Consume the next token or raise FormatError at the end."""
        nonlocal pos
        if pos >= len(tokens):
            raise FormatError(f"{name}: file ends inside {what}")
        tok = tokens[pos]
        pos += 1
        return tok

    def read_body(element: Element) -> None:
        """The `{ ... }` after an element's type."""
        expect("{")
        while True:
            aname = next_token("an element body")
            if aname == "}":
                return
            tname = next_token("an attribute")
            if tname == "elementid":
                element.id = uuid.UUID(next_token("an element id"))
            elif tname == "element":
                ref = next_token("an element reference")
                element.set(aname, AttrType.ELEMENT, None)
                if ref:
                    pending.append((element, aname, -1, uuid.UUID(ref)))
            elif tname == "element_array":
                expect("[")
                items: List[Any] = []
                while True:
                    tok = next_token("an element array")
                    if tok == "]":
                        break
                    if tok == ",":
                        continue
                    if tok == "element":
                        ref = next_token("an element reference")
                        items.append(None)
                        if ref:
                            pending.append((element, aname, len(items) - 1, uuid.UUID(ref)))
                    else:
                        items.append(read_element(tok))
                element.set(aname, AttrType.ELEMENT + ARRAY_OFFSET, items)
            elif tname.endswith("_array"):
                kind = type_id(tname)
                expect("[")
                items = []
                while True:
                    tok = next_token("an array")
                    if tok == "]":
                        break
                    if tok != ",":
                        items.append(_kv2_scalar(kind - ARRAY_OFFSET, tok))
                element.set(aname, kind, items)
            elif tname in TYPE_IDS:
                kind = type_id(tname)
                value = _kv2_scalar(kind, next_token("a value"))
                if aname == "name" and kind == AttrType.STRING:
                    element.name = value          # the binary form keeps it in the header
                else:
                    element.set(aname, kind, value)
            else:
                # an inline child element: the type is on the attribute's line
                element.set(aname, AttrType.ELEMENT, read_element(tname))

    def read_element(etype: str) -> Element:
        """Read an element body into a new element."""
        element = Element(etype, "")
        doc.add(element)
        read_body(element)
        return element

    while pos < len(tokens):
        read_element(next_token("the file"))

    by_id = {element.id: element for element in doc.elements}
    for element, aname, index, ref in pending:
        target = by_id.get(ref, ref)             # an unknown id stays as an external stub
        attr = element.attribute(aname)
        if index < 0:
            attr.value = target
        else:
            attr.value[index] = target
    return doc


def _kv2_text(kind: int, v: Any) -> str:
    if kind == AttrType.INT:
        return str(int(v))
    if kind == AttrType.FLOAT:
        return repr(float(v)) if not float(v).is_integer() else str(int(v))
    if kind == AttrType.BOOL:
        return "1" if v else "0"
    if kind == AttrType.STRING:
        return v
    if kind == AttrType.BINARY:
        return v.hex()
    if kind == AttrType.TIME:
        return repr(v.seconds) if isinstance(v, Time) else repr(float(v))
    if kind == AttrType.COLOR:
        return " ".join(str(int(c)) for c in v)
    if kind in _S_VEC:
        return " ".join(_kv2_text(AttrType.FLOAT, c) for c in v)
    raise FormatError(f"keyvalues2: cannot write a {type_name(kind)}")


def _quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _serialise_kv2(doc: DmxDocument) -> bytes:
    lines: List[str] = [f"<!-- dmx encoding keyvalues2 {doc.encoding_version} format {doc.format} {doc.format_version} -->"]
    # an element is written in full the first time it is met, by id afterwards
    written: set = set()

    def reference(v: Any) -> str:
        """An element or GUID as its GUID string."""
        return str(v if isinstance(v, uuid.UUID) else v.id)

    def write_body(element: Element, depth: int) -> None:
        """Write an element and, inline, the elements only it refers to."""
        written.add(id(element))
        indent = "\t" * depth
        inner = indent + "\t"
        lines.append(f"{indent}{{")
        lines.append(f'{inner}"id" "elementid" "{element.id}"')
        if element.name:
            lines.append(f'{inner}"name" "string" {_quote(element.name)}')
        for a in element:
            if a.type == AttrType.ELEMENT:
                v = a.value
                if v is None:
                    lines.append(f'{inner}{_quote(a.name)} "element" ""')
                elif isinstance(v, uuid.UUID) or id(v) in written:
                    lines.append(f'{inner}{_quote(a.name)} "element" "{reference(v)}"')
                else:
                    lines.append(f"{inner}{_quote(a.name)} {_quote(v.type)}")
                    write_body(v, depth + 1)
                    lines.append(inner)                  # Valve leaves an indented blank line here
            elif a.type == AttrType.ELEMENT + ARRAY_OFFSET:
                lines.append(f'{inner}{_quote(a.name)} "element_array" ')      # Valve leaves this space
                lines.append(f"{inner}[")
                for i, v in enumerate(a.value):
                    comma = "," if i < len(a.value) - 1 else ""
                    if v is None:
                        lines.append(f'{inner}\t"element" ""{comma}')
                    elif isinstance(v, uuid.UUID) or id(v) in written:
                        lines.append(f'{inner}\t"element" "{reference(v)}"{comma}')
                    else:
                        lines.append(f"{inner}\t{_quote(v.type)}")
                        write_body(v, depth + 2)
                        lines[-1] += comma
                lines.append(f"{inner}]")
            elif a.is_array:
                base = a.type - ARRAY_OFFSET
                lines.append(f'{inner}{_quote(a.name)} "{a.type_name}" ')
                lines.append(f"{inner}[")
                for i, v in enumerate(a.value):
                    comma = "," if i < len(a.value) - 1 else ""
                    lines.append(f"{inner}\t{_quote(_kv2_text(base, v))}{comma}")
                lines.append(f"{inner}]")
            else:
                lines.append(f'{inner}{_quote(a.name)} "{a.type_name}" {_quote(_kv2_text(a.type, a.value))}')
        lines.append(f"{indent}}}")

    for element in doc.elements:
        if id(element) not in written:
            lines.append(_quote(element.type))
            write_body(element, 0)
    lines.append("")                                   # the file ends with a blank line
    return (doc.line_ending.join(lines) + doc.line_ending).encode("utf-8", "surrogateescape")


# ===========================================================================
#  Entry points
# ===========================================================================
def parse_dmx(data: bytes, name: str = "file.dmx") -> DmxDocument:
    """Parse binary or keyvalues2 DMX bytes."""
    header = read_header(data, name)
    if header.encoding == "binary":
        return _parse_binary(data, header, name)
    if header.encoding == "keyvalues2":
        return _parse_kv2(data, header, name)
    raise FormatError(f"{name}: encoding {header.encoding!r} is not supported")


def serialise_dmx(doc: DmxDocument) -> bytes:
    """Bytes in the document's own encoding and version."""
    if doc.encoding == "binary":
        return _serialise_binary(doc)
    if doc.encoding == "keyvalues2":
        return _serialise_kv2(doc)
    raise FormatError(f"encoding {doc.encoding!r} is not supported")


def load_dmx(path: Union[str, Path]) -> DmxDocument:
    """Parse a .dmx file."""
    path = Path(path)
    return parse_dmx(path.read_bytes(), path.name)


def save_dmx(doc: DmxDocument, path: Union[str, Path]) -> None:
    """Write a document to a .dmx file."""
    Path(path).write_bytes(serialise_dmx(doc))
