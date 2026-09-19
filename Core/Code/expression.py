"""
The little expression language of DmeExpressionOperator.

    lerp(value, lo, hi)
    7 * noise(4 * time, 0, 0)
    max(0, (footRoll - 0.5)) * 140

Numbers, the usual arithmetic with precedence and parentheses, comparison
and boolean operators, a `?:` conditional, and a set of functions. Names
that are not functions are variables the caller supplies - an operator's
own attributes, plus `time`.

    value = evaluate("lerp(value, lo, hi)", {"value": 0.5, "lo": 10, "hi": 120})
"""
from __future__ import annotations

import math
import re
from typing import Callable, Dict, List, Mapping, Optional

__all__ = ["evaluate", "ExpressionError", "compile_expression"]


class ExpressionError(ValueError):
    pass


_TOKEN = re.compile(r"\s*(?:(\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+)|([A-Za-z_]\w*)|(<=|>=|==|!=|&&|\|\||[-+*/%^(),<>?:!]))")


def _noise(x: float) -> float:
    """A smooth pseudo-random function of one variable in -1..1, repeatable."""
    i = math.floor(x)
    f = x - i
    f = f * f * (3.0 - 2.0 * f)
    a = _hash(i)
    b = _hash(i + 1)
    return a + (b - a) * f


def _hash(i: int) -> float:
    n = (i * 1103515245 + 12345) & 0x7FFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0x7FFFFFFF
    return (n & 0xFFFF) / 32767.5 - 1.0


def _clamp(v: float, lo: float, hi: float) -> float:
    return lo if v < lo else hi if v > hi else v


_FUNCTIONS: Dict[str, Callable[..., float]] = {
    "abs": abs, "min": min, "max": max, "sqrt": lambda x: math.sqrt(x) if x > 0 else 0.0,
    "sqr": lambda x: x * x, "pow": lambda a, b: math.pow(a, b), "exp": math.exp,
    "log": lambda x: math.log(x) if x > 0 else 0.0,
    "sin": math.sin, "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos,
    "atan": math.atan, "atan2": math.atan2,
    "floor": math.floor, "ceil": math.ceil, "round": lambda x: float(round(x)),
    "sign": lambda x: 1.0 if x > 0 else -1.0 if x < 0 else 0.0,
    "dtor": math.radians, "rtod": math.degrees,
    "clamp": _clamp,
    "lerp": lambda t, a, b: a + (b - a) * t,
    "inrange": lambda x, lo, hi: 1.0 if lo <= x <= hi else 0.0,
    "rescale": lambda x, a, b, c, d: c + (d - c) * ((x - a) / (b - a) if b != a else 0.0),
    "ramp": lambda x, a, b: _clamp((x - a) / (b - a), 0.0, 1.0) if b != a else 0.0,
    "cramp": lambda x, a, b: _clamp((x - a) / (b - a), 0.0, 1.0) if b != a else 0.0,
    "elerp": lambda t, a, b: a + (b - a) * (t * t * (3 - 2 * t)),
    "noise": lambda x, y=0.0, z=0.0: _noise(x + y * 57.0 + z * 131.0),
    "cnoise": lambda x, y=0.0, z=0.0: _noise(x + y * 57.0 + z * 131.0) * 0.5 + 0.5,
}


class _Parser:
    def __init__(self, text: str) -> None:
        self.tokens: List[str] = []
        pos = 0
        while pos < len(text):
            m = _TOKEN.match(text, pos)
            if not m or m.end() == pos:
                if text[pos:].strip() == "":
                    break
                raise ExpressionError(f"cannot read {text[pos:pos + 10]!r}")
            pos = m.end()
            self.tokens.append(next(g for g in m.groups() if g is not None))
        self.pos = 0

    def peek(self) -> Optional[str]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self, expected: Optional[str] = None) -> str:
        tok = self.peek()
        if tok is None or (expected is not None and tok != expected):
            raise ExpressionError(f"expected {expected!r}, got {tok!r}")
        self.pos += 1
        return tok

    # grammar, lowest precedence first
    def conditional(self, v):
        cond = self.or_(v)
        if self.peek() == "?":
            self.take()
            a = self.conditional(v)
            self.take(":")
            b = self.conditional(v)
            return a if cond else b
        return cond

    def or_(self, v):
        left = self.and_(v)
        while self.peek() == "||":
            self.take(); right = self.and_(v)
            left = 1.0 if (left or right) else 0.0
        return left

    def and_(self, v):
        left = self.equality(v)
        while self.peek() == "&&":
            self.take(); right = self.equality(v)
            left = 1.0 if (left and right) else 0.0
        return left

    def equality(self, v):
        left = self.comparison(v)
        while self.peek() in ("==", "!="):
            op = self.take(); right = self.comparison(v)
            left = 1.0 if ((left == right) if op == "==" else (left != right)) else 0.0
        return left

    def comparison(self, v):
        left = self.additive(v)
        while self.peek() in ("<", ">", "<=", ">="):
            op = self.take(); right = self.additive(v)
            left = 1.0 if {"<": left < right, ">": left > right, "<=": left <= right, ">=": left >= right}[op] else 0.0
        return left

    def additive(self, v):
        left = self.term(v)
        while self.peek() in ("+", "-"):
            op = self.take(); right = self.term(v)
            left = left + right if op == "+" else left - right
        return left

    def term(self, v):
        left = self.power(v)
        while self.peek() in ("*", "/", "%"):
            op = self.take(); right = self.power(v)
            if op == "*":
                left = left * right
            elif op == "/":
                left = left / right if right != 0 else 0.0
            else:
                left = math.fmod(left, right) if right != 0 else 0.0
        return left

    def power(self, v):
        base = self.unary(v)
        if self.peek() == "^":
            self.take()
            exponent = self.power(v)
            try:
                return math.pow(base, exponent)
            except (ValueError, OverflowError):
                return 0.0
        return base

    def unary(self, v):
        tok = self.peek()
        if tok == "-":
            self.take(); return -self.unary(v)
        if tok == "+":
            self.take(); return self.unary(v)
        if tok == "!":
            self.take(); return 0.0 if self.unary(v) else 1.0
        return self.primary(v)

    def primary(self, v):
        tok = self.take()
        if tok == "(":
            value = self.conditional(v)
            self.take(")")
            return value
        if tok[0].isdigit() or tok[0] == ".":
            return float(tok)
        if tok[0].isalpha() or tok[0] == "_":
            if self.peek() == "(":
                self.take("(")
                args = []
                if self.peek() != ")":
                    args.append(self.conditional(v))
                    while self.peek() == ",":
                        self.take(); args.append(self.conditional(v))
                self.take(")")
                fn = _FUNCTIONS.get(tok.lower())
                if fn is None:
                    raise ExpressionError(f"unknown function {tok!r}")
                try:
                    return float(fn(*args))
                except TypeError as exc:
                    raise ExpressionError(f"{tok}: {exc}") from exc
            value = v.get(tok)
            if value is None:
                value = v.get(tok.lower(), 0.0)
            return float(value)
        raise ExpressionError(f"unexpected {tok!r}")


def evaluate(text: str, variables: Mapping[str, float]) -> float:
    """Evaluate `text` with `variables`; a name not supplied reads as 0."""
    parser = _Parser(text)
    if not parser.tokens:
        return 0.0
    value = parser.conditional(variables)
    if parser.peek() is not None:
        raise ExpressionError(f"unexpected {parser.peek()!r} after the expression")
    return value


def compile_expression(text: str) -> Callable[[Mapping[str, float]], float]:
    """The same, tokenised once for repeated evaluation."""
    parser = _Parser(text)
    tokens = list(parser.tokens)

    def run(variables: Mapping[str, float]) -> float:
        parser.tokens = tokens
        parser.pos = 0
        if not tokens:
            return 0.0
        value = parser.conditional(variables)
        if parser.peek() is not None:
            raise ExpressionError(f"unexpected {parser.peek()!r} after the expression")
        return value
    return run
