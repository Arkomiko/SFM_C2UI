"""
Valve KeyValues (KV1) reader.

KV1 is the text format behind `gameinfo.txt`, `.vmt` materials, soundscripts and
most other loose Valve data, so every bridge starts here.

    kv = load(path)
    kv["FileSystem"]["SearchPaths"]
    kv.get_str("game")

Duplicate keys are meaningful in KV1 - a SearchPaths block repeats the key
"Game" once per mount - so entries are kept as an ordered list of pairs.
Lookups return the first match; :meth:`KeyValues.all` returns every one.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator, List, Optional, Tuple, Union

__all__ = ["KeyValues", "KeyValuesError", "loads", "load"]

Value = Union[str, "KeyValues"]

#: Encodings seen in Valve data files, tried in this order.
_ENCODINGS = ("utf-8", "utf-8-sig", "cp1252", "latin-1")

_ESCAPES = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}


class KeyValuesError(ValueError):
    """Raised when a document is malformed beyond recovery."""


class KeyValues:
    """An ordered, duplicate-tolerant KeyValues block."""

    __slots__ = ("name", "_pairs")

    def __init__(self, name: str = "", pairs: Optional[List[Tuple[str, Value]]] = None) -> None:
        self.name = name
        self._pairs: List[Tuple[str, Value]] = pairs if pairs is not None else []

    # -- building ---------------------------------------------------------------
    def append(self, key: str, value: Value) -> None:
        self._pairs.append((key, value))

    # -- lookup -----------------------------------------------------------------
    def _find(self, key: str) -> Iterator[Value]:
        lowered = key.lower()
        for k, v in self._pairs:
            if k.lower() == lowered:
                yield v

    def __contains__(self, key: str) -> bool:
        return next(self._find(key), None) is not None

    def __getitem__(self, key: str) -> Value:
        value = next(self._find(key), None)
        if value is None:
            raise KeyError(key)
        return value

    def get(self, key: str, default: Any = None) -> Any:
        return next(self._find(key), default)

    def all(self, key: str) -> List[Value]:
        """Every value stored under `key` - KV1 allows repeats."""
        return list(self._find(key))

    def get_str(self, key: str, default: str = "") -> str:
        value = next(self._find(key), None)
        return value if isinstance(value, str) else default

    def get_int(self, key: str, default: int = 0) -> int:
        try:
            return int(self.get_str(key, "").strip())
        except ValueError:
            return default

    def block(self, key: str) -> Optional["KeyValues"]:
        """The first nested block under `key`, or None."""
        for value in self._find(key):
            if isinstance(value, KeyValues):
                return value
        return None

    def path(self, *keys: str) -> Optional["KeyValues"]:
        """Walk nested blocks: ``kv.path("FileSystem", "SearchPaths")``."""
        node: Optional[KeyValues] = self
        for key in keys:
            if node is None:
                return None
            node = node.block(key)
        return node

    # -- iteration --------------------------------------------------------------
    def items(self) -> List[Tuple[str, Value]]:
        return list(self._pairs)

    def keys(self) -> List[str]:
        return [k for k, _ in self._pairs]

    def pairs(self) -> List[Tuple[str, str]]:
        """Only the string entries, in order - what SearchPaths needs."""
        return [(k, v) for k, v in self._pairs if isinstance(v, str)]

    def __iter__(self) -> Iterator[Tuple[str, Value]]:
        return iter(self._pairs)

    def __len__(self) -> int:
        return len(self._pairs)

    def __repr__(self) -> str:
        return f"KeyValues({self.name!r}, {len(self._pairs)} entries)"


# ---------------------------------------------------------------------------
#  Parsing
# ---------------------------------------------------------------------------
class _Tokenizer:
    """Quoted strings, bare strings and braces; `//` and `/* */` comments.

    Escape sequences are **off by default**, matching Valve's own parser: game
    data is full of Windows paths like ``models\\tf\\player.mdl``, and treating
    ``\\t`` as a tab would quietly corrupt every one of them.
    """

    __slots__ = ("text", "pos", "size", "escapes")

    def __init__(self, text: str, escapes: bool = False) -> None:
        self.text = text
        self.pos = 0
        self.size = len(text)
        self.escapes = escapes

    def _skip(self, i: int) -> int:
        text, size = self.text, self.size
        while i < size:
            c = text[i]
            if c in " \t\r\n":
                i += 1
            elif c == "/" and i + 1 < size and text[i + 1] == "/":
                while i < size and text[i] != "\n":
                    i += 1
            elif c == "/" and i + 1 < size and text[i + 1] == "*":
                end = text.find("*/", i + 2)
                i = size if end < 0 else end + 2
            else:
                break
        return i

    def next(self) -> Optional[str]:
        text, size = self.text, self.size
        i = self._skip(self.pos)
        if i >= size:
            self.pos = i
            return None
        c = text[i]
        if c in "{}":
            self.pos = i + 1
            return c
        if c == '"':
            i += 1
            out: List[str] = []
            while i < size:
                ch = text[i]
                if ch == "\\" and self.escapes and i + 1 < size:
                    nxt = text[i + 1]
                    out.append(_ESCAPES.get(nxt, "\\" + nxt))
                    i += 2
                    continue
                if ch == '"':
                    i += 1
                    break
                out.append(ch)
                i += 1
            self.pos = i
            return "".join(out)
        start = i
        while i < size and text[i] not in ' \t\r\n"{}':
            i += 1
        self.pos = i
        return text[start:i]

    def peek(self) -> Optional[str]:
        saved = self.pos
        token = self.next()
        self.pos = saved
        return token


def _parse_block(tok: _Tokenizer, name: str, depth: int) -> KeyValues:
    if depth > 64:
        raise KeyValuesError("KeyValues nested too deeply")
    kv = KeyValues(name)
    while True:
        key = tok.next()
        if key is None or key == "}":
            return kv
        if key == "{":
            # an anonymous block: keep it under an empty key rather than failing
            kv.append("", _parse_block(tok, "", depth + 1))
            continue
        nxt = tok.peek()
        if nxt == "{":
            tok.next()
            kv.append(key, _parse_block(tok, key, depth + 1))
        elif nxt is None:
            kv.append(key, "")
            return kv
        else:
            value = tok.next()
            if value == "}":                 # a key with no value ends the block
                kv.append(key, "")
                return kv
            kv.append(key, value or "")


def loads(text: str, name: str = "", escapes: bool = False) -> KeyValues:
    """Parse KeyValues text.  A single outer block is unwrapped.

    `escapes` follows Valve: off by default, so backslashes stay literal and
    Windows paths survive. Turn it on only for a file known to need it.
    """
    if text.startswith("﻿"):
        text = text[1:]
    root = _parse_block(_Tokenizer(text, escapes), name, 0)
    if len(root) == 1:
        only_key, only_value = root.items()[0]
        if isinstance(only_value, KeyValues):
            only_value.name = only_key
            return only_value
    return root


def load(path: Union[str, Path], escapes: bool = False) -> KeyValues:
    """Read a KeyValues file, tolerating the mixed encodings in Valve data."""
    p = Path(path)
    raw = p.read_bytes()
    for enc in _ENCODINGS:
        try:
            return loads(raw.decode(enc), p.stem, escapes)
        except UnicodeDecodeError:
            continue
    return loads(raw.decode("latin-1", "replace"), p.stem, escapes)
