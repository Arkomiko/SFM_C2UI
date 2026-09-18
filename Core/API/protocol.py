# -*- coding: utf-8 -*-
"""
Wire protocol shared by the host (Python 3 / PySide6) and the in-SFM agent
(Python 2.7 / PySide 1.2).  Keep this file 2/3 compatible: no f-strings, no
annotations, no keyword-only arguments.

Transport: TCP on localhost, newline-delimited UTF-8 JSON objects.

Request  : {"id": 1, "method": "sfm.get_shots", "params": {...}}
Response : {"id": 1, "result": ...}             or  {"id": 1, "error": {"code": -1, "message": "..."}}
Event    : {"event": "sfm.selection_changed", "data": {...}}       (server -> client, no id)
"""
import json

PROTOCOL_VERSION = 1
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 41794
HANDSHAKE_METHOD = "c2ui.hello"

ERR_PARSE = -32700
ERR_METHOD_NOT_FOUND = -32601
ERR_INVALID_PARAMS = -32602
ERR_INTERNAL = -32603
ERR_SFM = -1000


def encode(obj):
    """Serialise a message to bytes terminated by a newline."""
    return (json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def decode(line):
    """Parse one line (bytes or str) into a dict."""
    if isinstance(line, bytes):
        line = line.decode("utf-8", "replace")
    return json.loads(line)


def make_request(req_id, method, params=None):
    return {"id": req_id, "method": method, "params": params or {}}


def make_result(req_id, result):
    return {"id": req_id, "result": result}


def make_error(req_id, code, message, data=None):
    err = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"id": req_id, "error": err}


def make_event(name, data=None):
    return {"event": name, "data": data or {}}
