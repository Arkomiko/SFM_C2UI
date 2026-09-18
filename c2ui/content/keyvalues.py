"""
Valve KeyValues (KV1) reader.

KV1 is the text format behind gameinfo.txt, .vmt materials, soundscripts and most
other loose Valve data files, so every content subsystem starts here.

    kv = loads(text)                 -> KeyValues
    kv["FileSystem"]["SearchPaths"]  -> nested KeyValues
    kv.get_str("game")               -> "Source Filmmaker [Beta]"

Duplicate keys are legal and meaningful in KV1 (a SearchPaths block repeats the
key "Game" for every mount), so values are kept as an ordered list of pairs and
lookups return the first match while :meth:`all` returns every one.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator, List, Optional, Tuple, Union

__all__ = ["KeyValues", "loads", "load"]

Value = Union[str, "KeyValues"]


class KeyValuesError(ValueError):
    """Raised when a KeyValues document is malformed beyond recovery."""


class KeyValues:
    """An ordered, duplicate-tolerant KeyValues block."""

    __slots__ = ("name", "_pairs")

    def __init__(self, name: str = "", pairs: Optional[List[Tuple[str, Value]]] = None) -> None:
        self.name = name
        self._pairs: List[Tuple[str, Value]] = pairs if pairs is not None else []

    # -- construction ----------------------------------------------------------
    def append(self, key: str, value: Value) -> None:
        self._pairs.append((key, value))

    # -- lookup ----------------------------------------------------------------
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
        """Every value stored under ``key`` - KV1 allows repeats."""
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
        for value in self._find(key):
            if isinstance(value, KeyValues):
                return value
        return None

    # -- iteration -------------------------------------------------------------
    def items(self) -> List[Tuple[str, Value]]:
        return list(self._pairs)

    def keys(self) -> List[str]:
        return [k for k, _ in self._pairs]

    def __iter__(self) -> Iterator[Tuple[str, Value]]:
        return iter(self._pairs)

    def __len__(self) -> int:
        return len(self._pairs)

    def __repr__(self) -> str:
        return f"KeyValues({self.name!r}, {len(self._pairs)} entries)"


# ---------------------------------------------------------------------------
#  Parser
# ---------------------------------------------------------------------------
class _Tokenizer:
    """KV1 tokens: quoted strings, bare strings, braces; // and /* */ comments."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.size = len(text)

    def next(self) -> Optional[str]:
        text, size = self.text, self.size
        i = self.pos
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
        if i >= size:
            self.pos = i
            return None
        c = text[i]
        if c in "{}":
            self.pos = i + 1
            return c
        if c == '"':
            i += 1
            out = []
            while i < size:
                ch = text[i]
                if ch == "\\" and i + 1 < size:
                    nxt = text[i + 1]
                    # Valve only escapes these; a lone backslash is a path separator
                    out.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\"}.get(nxt, "\\" + nxt))
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
            # anonymous block - keep it under an empty key rather than failing
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
            if value == "}":          # key with no value at the end of a block
                kv.append(key, "")
                return kv
            kv.append(key, value if value is not None else "")


def loads(text: str, name: str = "") -> KeyValues:
    """Parse KeyValues text.  The outer block is unwrapped when there is exactly one."""
    if text.startswith("﻿"):
        text = text[1:]
    tok = _Tokenizer(text)
    root = _parse_block(tok, name, 0)
    if len(root) == 1:
        only_key, only_value = root.items()[0]
        if isinstance(only_value, KeyValues):
            only_value.name = only_key
            return only_value
    return root


def load(path: Union[str, Path], encoding: str = "utf-8") -> KeyValues:
    """Read a KeyValues file, tolerating the mixed encodings found in Valve data."""
    raw = Path(path).read_bytes()
    for enc in (encoding, "utf-8-sig", "cp1252", "latin-1"):
        try:
            return loads(raw.decode(enc), Path(path).stem)
        except UnicodeDecodeError:
            continue
    return loads(raw.decode("latin-1", "replace"), Path(path).stem)
