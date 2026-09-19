"""
The Datamodel: what a Source Filmmaker session is made of.

A .dmx file is a graph of elements. Every element has a type, a name, a GUID
and an ordered set of attributes; an attribute holds one value or an array of
values of a single type, and a value may itself be an element, which is how the
graph is built. Sessions, particle systems, compiled DMX models and SFM's own
presets are all this one structure with different element types in it.

    doc = load_dmx(path)                     # Core.Code.formats.dmx
    doc.root["activeClip"]["name"]
    for element in doc.elements: ...
    save_dmx(doc, path)                      # byte for byte what was read

Values are plain Python: int, float, bool, str, bytes, tuples for vectors and
colours, Time for the timeline's fixed-point seconds, Element for references
and None for a null reference. Arrays are lists.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional, Tuple

__all__ = [
    "AttrType", "Time", "Element", "Attribute", "DmxDocument",
    "Color", "Vector2", "Vector3", "Vector4", "QAngle", "Quaternion", "Matrix",
    "ARRAY_OFFSET", "TYPE_NAMES",
]

Color = Tuple[int, int, int, int]
Vector2 = Tuple[float, float]
Vector3 = Tuple[float, float, float]
Vector4 = Tuple[float, float, float, float]
QAngle = Tuple[float, float, float]
Quaternion = Tuple[float, float, float, float]
Matrix = Tuple[float, ...]                 # 16 values, row-major as stored


class AttrType:
    """Attribute type ids as stored in binary files.  Arrays are +14."""
    ELEMENT = 1
    INT = 2
    FLOAT = 3
    BOOL = 4
    STRING = 5
    BINARY = 6
    TIME = 7               # ObjectID in binary encodings before 3
    COLOR = 8
    VECTOR2 = 9
    VECTOR3 = 10
    VECTOR4 = 11
    QANGLE = 12
    QUATERNION = 13
    MATRIX = 14


ARRAY_OFFSET = 14

TYPE_NAMES: Dict[int, str] = {
    AttrType.ELEMENT: "element", AttrType.INT: "int", AttrType.FLOAT: "float",
    AttrType.BOOL: "bool", AttrType.STRING: "string", AttrType.BINARY: "binary",
    AttrType.TIME: "time", AttrType.COLOR: "color", AttrType.VECTOR2: "vector2",
    AttrType.VECTOR3: "vector3", AttrType.VECTOR4: "vector4", AttrType.QANGLE: "qangle",
    AttrType.QUATERNION: "quaternion", AttrType.MATRIX: "matrix",
}
TYPE_IDS: Dict[str, int] = {v: k for k, v in TYPE_NAMES.items()}


def type_name(type_id: int) -> str:
    if type_id > ARRAY_OFFSET:
        return TYPE_NAMES[type_id - ARRAY_OFFSET] + "_array"
    return TYPE_NAMES[type_id]


def type_id(name: str) -> int:
    if name.endswith("_array"):
        return TYPE_IDS[name[:-6]] + ARRAY_OFFSET
    return TYPE_IDS[name]


def is_array(type_id_: int) -> bool:
    return type_id_ > ARRAY_OFFSET


class Time:
    """A moment on the timeline, in ten-thousandths of a second.

    Stored as an integer so a value read from a file is written back exactly;
    a float would round.
    """

    __slots__ = ("ticks",)
    PER_SECOND = 10000

    def __init__(self, ticks: int = 0) -> None:
        self.ticks = int(ticks)

    @classmethod
    def from_seconds(cls, seconds: float) -> "Time":
        return cls(round(seconds * cls.PER_SECOND))

    @property
    def seconds(self) -> float:
        return self.ticks / self.PER_SECOND

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Time) and other.ticks == self.ticks

    def __hash__(self) -> int:
        return hash(self.ticks)

    def __lt__(self, other: "Time") -> bool:
        return self.ticks < other.ticks

    def __repr__(self) -> str:
        return f"Time({self.seconds:g}s)"


@dataclass
class Attribute:
    name: str
    type: int
    value: Any

    @property
    def is_array(self) -> bool:
        return is_array(self.type)

    @property
    def type_name(self) -> str:
        return type_name(self.type)


class Element:
    """One node of the graph: type, name, GUID and ordered attributes.

    Attributes are reached like a dictionary - ``element["name"]`` gives the
    value, ``element.attribute("name")`` the Attribute with its type.
    """

    __slots__ = ("type", "name", "id", "_attributes")

    def __init__(self, type: str = "DmElement", name: str = "",
                 id: Optional[uuid.UUID] = None) -> None:
        self.type = type
        self.name = name
        self.id = id if id is not None else uuid.uuid4()
        self._attributes: Dict[str, Attribute] = {}

    # -- attributes ------------------------------------------------------------------
    def attribute(self, name: str) -> Optional[Attribute]:
        return self._attributes.get(name)

    def attributes(self) -> List[Attribute]:
        return list(self._attributes.values())

    def set(self, name: str, type: int, value: Any) -> Attribute:
        attr = self._attributes.get(name)
        if attr is None:
            attr = Attribute(name, type, value)
            self._attributes[name] = attr
        else:
            attr.type = type
            attr.value = value
        return attr

    def remove(self, name: str) -> bool:
        return self._attributes.pop(name, None) is not None

    def get(self, name: str, default: Any = None) -> Any:
        attr = self._attributes.get(name)
        return attr.value if attr is not None else default

    def __getitem__(self, name: str) -> Any:
        return self._attributes[name].value

    def __contains__(self, name: str) -> bool:
        return name in self._attributes

    def __iter__(self) -> Iterator[Attribute]:
        return iter(self._attributes.values())

    def __len__(self) -> int:
        return len(self._attributes)

    def __repr__(self) -> str:
        return f"<{self.type} {self.name!r} {len(self._attributes)} attrs>"


@dataclass
class DmxDocument:
    """A whole file: its encoding, format and every element in file order."""

    encoding: str = "binary"
    encoding_version: int = 5
    format: str = "dmx"
    format_version: int = 18
    #: every element, in the order the file lists them; the first is the root
    elements: List[Element] = field(default_factory=list)
    #: the string table as read, so an unchanged file writes back identically
    strings: List[str] = field(default_factory=list)
    #: line ending of a text file as read; binary files ignore it
    line_ending: str = "\n"

    @property
    def root(self) -> Optional[Element]:
        return self.elements[0] if self.elements else None

    def find(self, type: Optional[str] = None, name: Optional[str] = None) -> List[Element]:
        return [e for e in self.elements
                if (type is None or e.type == type) and (name is None or e.name == name)]

    def by_id(self, id: uuid.UUID) -> Optional[Element]:
        for element in self.elements:
            if element.id == id:
                return element
        return None

    def add(self, element: Element) -> Element:
        self.elements.append(element)
        return element

    def summary(self) -> str:
        types = {}
        for e in self.elements:
            types[e.type] = types.get(e.type, 0) + 1
        top = ", ".join(f"{t} x{n}" for t, n in sorted(types.items(), key=lambda kv: -kv[1])[:5])
        return (f"{self.encoding} {self.encoding_version} / {self.format} {self.format_version}: "
                f"{len(self.elements)} elements ({top})")
