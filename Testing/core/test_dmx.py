"""
DMX: the datamodel, both encodings, every binary version, written back exactly.
"""
import struct
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Core.API.dmx import ARRAY_OFFSET, AttrType, DmxDocument, Element, Time
from Core.Code.formats import FormatError
from Core.Code.formats.dmx import parse_dmx, read_header, serialise_dmx

GUID_A = uuid.UUID("11111111-2222-3333-4444-555555555555")
GUID_B = uuid.UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")


def _sample(encoding="binary", version=5):
    doc = DmxDocument(encoding=encoding, encoding_version=version, format="sfm_session",
                      format_version=20)
    root = doc.add(Element("DmElement", "session", GUID_A))
    child = doc.add(Element("DmeClip", "clip", GUID_B))
    root.set("activeClip", AttrType.ELEMENT, child)
    root.set("count", AttrType.INT, -7)
    root.set("scale", AttrType.FLOAT, 0.5)
    root.set("visible", AttrType.BOOL, True)
    root.set("title", AttrType.STRING, "Hello \"world\"")
    root.set("blob", AttrType.BINARY, b"\x00\x01\x02")
    root.set("color", AttrType.COLOR, (255, 128, 0, 255))
    root.set("pos", AttrType.VECTOR3, (1.0, 2.0, 3.0))
    root.set("rot", AttrType.QUATERNION, (0.0, 0.0, 0.0, 1.0))
    root.set("tags", AttrType.STRING + ARRAY_OFFSET, ["a", "b", "c"])
    root.set("values", AttrType.FLOAT + ARRAY_OFFSET, [1.5, 2.5])
    root.set("children", AttrType.ELEMENT + ARRAY_OFFSET, [child, None])
    root.set("nothing", AttrType.ELEMENT, None)
    if version >= 3 or encoding != "binary":
        root.set("start", AttrType.TIME, Time(12345))
    child.set("name_copy", AttrType.STRING, "clip")
    return doc


def _same(a: DmxDocument, b: DmxDocument) -> None:
    assert [(e.type, e.name, e.id) for e in a.elements] == [(e.type, e.name, e.id) for e in b.elements]
    for ea, eb in zip(a.elements, b.elements):
        assert [x.name for x in ea] == [x.name for x in eb], (ea, eb)
        for x, y in zip(ea, eb):
            assert x.type == y.type, x.name
            if x.type == AttrType.ELEMENT:
                assert (x.value.id if x.value else None) == (y.value.id if y.value else None)
            elif x.type == AttrType.ELEMENT + ARRAY_OFFSET:
                assert [v.id if v else None for v in x.value] == [v.id if v else None for v in y.value]
            elif x.type == AttrType.FLOAT:
                assert abs(x.value - y.value) < 1e-6
            else:
                assert x.value == y.value, (x.name, x.value, y.value)


# ------------------------------------------------------------------- header
def test_header_is_read():
    h = read_header(b"<!-- dmx encoding binary 5 format sfm_session 20 -->\n\0")
    assert (h.encoding, h.encoding_version, h.format, h.format_version) == ("binary", 5, "sfm_session", 20)


def test_not_a_dmx_file():
    for bad in (b"", b"IDST", b"<!-- dmx encoding -->\n"):
        try:
            parse_dmx(bad, "x")
        except FormatError:
            continue
        raise AssertionError(bad)


# ------------------------------------------------------------------- binary
def test_every_binary_version_round_trips():
    for version in (1, 2, 3, 4, 5):
        doc = _sample("binary", version)
        data = serialise_dmx(doc)
        assert data.startswith(f"<!-- dmx encoding binary {version} format sfm_session 20 -->\n\0".encode())
        back = parse_dmx(data, f"v{version}")
        assert back.encoding_version == version
        _same(doc, back)
        assert serialise_dmx(back) == data, version         # and again, byte for byte


def test_binary_5_layout_is_exactly_what_the_engine_writes():
    """A file assembled by hand: string table, headers, attributes."""
    strings = [b"DmElement", b"root", b"count", b"title", b"hi"]
    data = bytearray(b"<!-- dmx encoding binary 5 format dmx 18 -->\n\0")
    data += struct.pack("<i", len(strings))
    for s in strings:
        data += s + b"\0"
    data += struct.pack("<i", 1)                          # one element
    data += struct.pack("<ii", 0, 1) + GUID_A.bytes_le    # type, name, id
    data += struct.pack("<i", 2)                          # two attributes
    data += struct.pack("<i", 2) + bytes([AttrType.INT]) + struct.pack("<i", 42)
    data += struct.pack("<i", 3) + bytes([AttrType.STRING]) + struct.pack("<i", 4)
    doc = parse_dmx(bytes(data), "hand.dmx")
    assert doc.root.type == "DmElement" and doc.root.name == "root" and doc.root.id == GUID_A
    assert doc.root["count"] == 42 and doc.root["title"] == "hi"
    assert serialise_dmx(doc) == bytes(data)


def test_binary_2_uses_short_table_and_inline_names():
    data = serialise_dmx(_sample("binary", 2))
    body = data[data.index(b"\0") + 1:]
    count = struct.unpack_from("<h", body)[0]
    assert count > 0
    # the element name is not in the table: it appears inline after the type index
    assert b"session\0" in body[2:]


def test_time_is_exact_ticks_not_float():
    doc = _sample("binary", 5)
    doc.root.set("start", AttrType.TIME, Time(123457))
    back = parse_dmx(serialise_dmx(doc), "t")
    assert back.root["start"] == Time(123457)
    assert back.root["start"].seconds == 12.3457


def test_object_id_before_version_3():
    doc = DmxDocument(encoding="binary", encoding_version=2, format="pcf", format_version=1)
    doc.add(Element("DmElement", "x", GUID_A)).set("oid", AttrType.TIME, GUID_B)
    back = parse_dmx(serialise_dmx(doc), "oid")
    assert back.root["oid"] == GUID_B


def test_external_element_reference_survives():
    doc = _sample("binary", 5)
    doc.root.set("elsewhere", AttrType.ELEMENT, GUID_B)
    data = serialise_dmx(doc)
    back = parse_dmx(data, "ext")
    assert back.root["elsewhere"] == GUID_B
    assert serialise_dmx(back) == data


def test_string_table_order_is_preserved():
    doc = _sample("binary", 5)
    data = serialise_dmx(doc)
    back = parse_dmx(data, "s")
    assert back.strings[:2] == ["DmElement", "session"]
    back.root.set("count", AttrType.INT, 8)             # a change that adds no strings
    changed = serialise_dmx(back)
    assert len(changed) == len(data)
    assert changed[:data.index(b"\xf9\xff\xff\xff")] == data[:data.index(b"\xf9\xff\xff\xff")]


def test_truncated_file_is_reported_with_position():
    data = serialise_dmx(_sample("binary", 5))
    try:
        parse_dmx(data[:-10], "short")
    except FormatError as exc:
        assert "truncated" in str(exc) or "unterminated" in str(exc)
    else:
        raise AssertionError("truncated file accepted")


def test_reference_to_an_element_outside_the_document_is_refused():
    doc = _sample("binary", 5)
    doc.root.set("stray", AttrType.ELEMENT, Element("DmElement", "stray"))
    try:
        serialise_dmx(doc)
    except FormatError as exc:
        assert "not in the document" in str(exc)
    else:
        raise AssertionError("stray element written")


# ------------------------------------------------------------------- keyvalues2
# Valve's writer leaves a space after array types and an indented blank
# line after an inline child; the bytes below carry both
KV2 = b'''<!-- dmx encoding keyvalues2 1 format dmx 1 -->
"DmElement"
{
	"id" "elementid" "11111111-2222-3333-4444-555555555555"
	"name" "string" "root"
	"count" "int" "3"
	"ratio" "float" "0.25"
	"on" "bool" "1"
	"pos" "vector3" "1 2 3"
	"tags" "string_array" 
	[
		"a",
		"b"
	]
	"child" "DmeClip"
	{
		"id" "elementid" "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
		"name" "string" "clip"
		"back" "element" "11111111-2222-3333-4444-555555555555"
	}
	
	"kids" "element_array" 
	[
		"element" "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
		"element" ""
	]
}

'''


def test_keyvalues2_is_read():
    doc = parse_dmx(KV2, "text.dmx")
    root = doc.root
    assert root.type == "DmElement" and root.name == "root" and root.id == GUID_A
    assert root["count"] == 3 and root["ratio"] == 0.25 and root["on"] is True
    assert root["pos"] == (1.0, 2.0, 3.0)
    assert root["tags"] == ["a", "b"]
    child = root["child"]
    assert child.type == "DmeClip" and child.name == "clip" and child.id == GUID_B
    assert child["back"] is root                          # a reference resolved by id
    assert root["kids"] == [child, None]
    assert len(doc.elements) == 2


def test_keyvalues2_writes_back_what_it_read():
    doc = parse_dmx(KV2, "text.dmx")
    assert serialise_dmx(doc) == KV2


def test_keyvalues2_keeps_windows_line_endings():
    crlf = KV2.replace(b"\n", b"\r\n")
    doc = parse_dmx(crlf, "crlf.dmx")
    assert doc.line_ending == "\r\n"
    assert serialise_dmx(doc) == crlf


def test_keyvalues2_and_binary_hold_the_same_document():
    doc = parse_dmx(KV2, "text.dmx")
    doc.encoding, doc.encoding_version = "binary", 5
    back = parse_dmx(serialise_dmx(doc), "bin")
    _same(doc, back)


# ------------------------------------------------------------------- model
def test_element_behaves_like_a_record():
    e = Element("DmeCamera", "cam")
    e.set("fov", AttrType.FLOAT, 60.0)
    assert "fov" in e and e["fov"] == 60.0 and e.get("missing", 1) == 1
    assert e.attribute("fov").type_name == "float"
    e.set("fov", AttrType.INT, 70)
    assert e.attribute("fov").type == AttrType.INT and len(e) == 1
    assert e.remove("fov") and not e.remove("fov")


def test_document_lookups():
    doc = _sample()
    assert doc.by_id(GUID_B).name == "clip"
    assert [e.name for e in doc.find(type="DmeClip")] == ["clip"]
    assert "2 elements" in doc.summary()
