"""Lightweight HCL2 lexer + parser used by the static evaluation engine.

This is intentionally tolerant: it recovers from unknown tokens so the
evaluator can report meaningful syntax issues instead of crashing.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


class HCLError(Exception):
    pass


@dataclass
class Token:
    type: str
    value: str
    start: int
    end: int
    line: int


@dataclass
class Attr:
    name: str
    raw: str
    tokens: list[Token]
    line: int


@dataclass
class Block:
    type: str
    labels: list[str]
    attrs: list[Attr]
    blocks: list["Block"]
    line: int
    file: str = ""

    def attr(self, name: str) -> Optional[Attr]:
        for a in self.attrs:
            if a.name == name:
                return a
        return None

    def nested(self, btype: str) -> list["Block"]:
        return [b for b in self.blocks if b.type == btype]

    def all_nested(self, btype: str) -> list["Block"]:
        out: list[Block] = []
        for b in self.blocks:
            if b.type == btype:
                out.append(b)
            out.extend(b.all_nested(btype))
        return out


PUNCT = {
    "{": "LBRACE",
    "}": "RBRACE",
    "[": "LBRACK",
    "]": "RBRACK",
    "(": "LPAREN",
    ")": "RPAREN",
    "=": "EQUALS",
    ",": "COMMA",
    ".": "DOT",
    ":": "COLON",
    "?": "QUESTION",
    "+": "OP",
    "-": "OP",
    "*": "OP",
    "/": "OP",
    "%": "OP",
    "<": "OP",
    ">": "OP",
    "!": "OP",
    "&": "OP",
    "|": "OP",
    "~": "OP",
}


def tokenize(src: str) -> tuple[list[Token], list[tuple[int, str]]]:
    tokens: list[Token] = []
    errors: list[tuple[int, str]] = []
    i = 0
    line = 1
    n = len(src)

    while i < n:
        c = src[i]

        if c in " \t\f\v":
            i += 1
            continue
        if c == "\r":
            i += 1
            continue
        if c == "\n":
            tokens.append(Token("NEWLINE", "\n", i, i + 1, line))
            line += 1
            i += 1
            continue

        # comments
        if c == "#" or (c == "/" and i + 1 < n and src[i + 1] == "/"):
            while i < n and src[i] != "\n":
                i += 1
            continue
        if c == "/" and i + 1 < n and src[i + 1] == "*":
            j = src.find("*/", i + 2)
            if j == -1:
                errors.append((line, "Unterminated block comment"))
                i = n
            else:
                line += src.count("\n", i, j)
                i = j + 2
            continue

        # quoted string (with interpolation awareness)
        if c == '"':
            start = i
            i += 1
            buf: list[str] = []
            closed = False
            while i < n:
                ch = src[i]
                if ch == "\\":
                    if i + 1 < n:
                        buf.append(src[i : i + 2])
                        i += 2
                        continue
                    buf.append("\\")
                    i += 1
                    continue
                if ch == '"':
                    i += 1
                    closed = True
                    break
                if ch == "\n":
                    line += 1
                if ch == "$" and i + 1 < n and src[i + 1] == "{":
                    buf.append("${")
                    i += 2
                    depth = 1
                    while i < n and depth > 0:
                        c2 = src[i]
                        if c2 == '"':
                            buf.append('"')
                            i += 1
                            while i < n:
                                if src[i] == "\\":
                                    buf.append(src[i : i + 2])
                                    i += 2
                                    continue
                                if src[i] == '"':
                                    buf.append('"')
                                    i += 1
                                    break
                                if src[i] == "\n":
                                    line += 1
                                buf.append(src[i])
                                i += 1
                            continue
                        if c2 == "{":
                            depth += 1
                        elif c2 == "}":
                            depth -= 1
                        if c2 == "\n":
                            line += 1
                        buf.append(c2)
                        i += 1
                    continue
                buf.append(ch)
                i += 1
            if not closed:
                errors.append((line, "Unterminated string literal"))
            tokens.append(Token("STRING", "".join(buf), start, i, line))
            continue

        # heredoc
        if c == "<" and i + 1 < n and src[i + 1] == "<":
            start = i
            j = i + 2
            strip = False
            if j < n and src[j] == "-":
                strip = True
                j += 1
            if j < n and src[j] == '"':
                k = src.find('"', j + 1)
                if k == -1:
                    marker = src[j + 1 :]
                    j = n
                else:
                    marker = src[j + 1 : k]
                    j = k + 1
            else:
                k = j
                while k < n and (src[k].isalnum() or src[k] == "_"):
                    k += 1
                marker = src[j:k]
                j = k
            nl = src.find("\n", j)
            pos = n if nl == -1 else nl + 1
            end = n
            while pos <= n:
                le = src.find("\n", pos)
                if le == -1:
                    le = n
                lt = src[pos:le]
                cmp = lt.strip() if strip else lt.rstrip("\r")
                if cmp == marker:
                    end = le
                    break
                if le >= n:
                    break
                pos = le + 1
            tokens.append(Token("HEREDOC", src[start:end], start, end, line))
            line += src.count("\n", start, end)
            i = end
            continue

        # number
        if c.isdigit() or (c == "." and i + 1 < n and src[i + 1].isdigit()):
            m = re.match(r"\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", src[i:])
            if m:
                v = m.group(0)
                tokens.append(Token("NUMBER", v, i, i + len(v), line))
                i += len(v)
                continue

        # identifier
        if c.isalpha() or c == "_":
            j = i
            while j < n and (src[j].isalnum() or src[j] in "_-"):
                j += 1
            tokens.append(Token("IDENT", src[i:j], i, j, line))
            i = j
            continue

        two = src[i : i + 2]
        if two in ("==", "!=", ">=", "<=", "&&", "||", "=>"):
            tokens.append(Token("OP", two, i, i + 2, line))
            i += 2
            continue
        if c in PUNCT:
            tokens.append(Token(PUNCT[c], c, i, i + 1, line))
            i += 1
            continue

        errors.append((line, f"Unexpected character {c!r}"))
        i += 1

    tokens.append(Token("EOF", "", n, n, line))
    return tokens, errors


class Parser:
    def __init__(self, src: str, tokens: list[Token], filename: str = ""):
        self.src = src
        self.tokens = tokens
        self.pos = 0
        self.file = filename
        self.errors: list[tuple[int, str]] = []

    def peek(self) -> Optional[Token]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self) -> Token:
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def skip_newlines(self) -> None:
        while self.peek() and self.peek().type == "NEWLINE":
            self.pos += 1

    def parse(self) -> list[Block]:
        _, blocks = self.parse_body(False)
        return blocks

    def parse_body(self, expect_close: bool) -> tuple[list[Attr], list[Block]]:
        attrs: list[Attr] = []
        blocks: list[Block] = []

        while True:
            self.skip_newlines()
            t = self.peek()
            if t is None or t.type == "EOF":
                if expect_close:
                    self.errors.append((t.line if t else 0, "Unclosed block: missing '}'"))
                return attrs, blocks
            if t.type == "RBRACE":
                self.advance()
                if not expect_close:
                    self.errors.append((t.line, "Unexpected '}'"))
                    continue
                return attrs, blocks
            if t.type not in ("IDENT", "STRING"):
                self.errors.append((t.line, f"Unexpected token {t.value!r}"))
                self.advance()
                continue

            name_tok = self.advance()
            name = name_tok.value

            # block labels (strings; identifiers tolerated)
            labels: list[str] = []
            while True:
                nt = self.peek()
                if nt is None:
                    break
                if nt.type in ("STRING", "IDENT"):
                    labels.append(nt.value)
                    self.advance()
                    continue
                break

            nt = self.peek()
            if nt and nt.type == "LBRACE":
                self.advance()
                body_attrs, body_blocks = self.parse_body(True)
                blocks.append(
                    Block(name, labels, body_attrs, body_blocks, name_tok.line, self.file)
                )
            elif nt and nt.type == "EQUALS":
                self.advance()
                toks, raw = self._parse_expr()
                attrs.append(Attr(name, raw, toks, name_tok.line))
            elif nt and nt.type == "COLON":
                self.advance()
                toks, raw = self._parse_expr()
                attrs.append(Attr(name, raw, toks, name_tok.line))
            else:
                if nt is not None:
                    self.errors.append(
                        (nt.line, f"Expected '=' or '{{' after {name!r}")
                    )

        return attrs, blocks

    def _parse_expr(self) -> tuple[list[Token], str]:
        t0 = self.peek()
        toks: list[Token] = []
        depth = 0
        while True:
            t = self.peek()
            if t is None or t.type == "EOF":
                break
            if t.type == "NEWLINE" and depth == 0:
                break
            if t.type == "RBRACE" and depth == 0:
                break
            if t.type in ("LBRACE", "LBRACK", "LPAREN"):
                depth += 1
            elif t.type in ("RBRACE", "RBRACK", "RPAREN"):
                if depth == 0:
                    break
                depth -= 1
            toks.append(t)
            self.advance()

        if toks:
            raw = self.src[toks[0].start : toks[-1].end].strip()
            return toks, raw
        return [], ""


@dataclass
class Config:
    files: dict[str, str]
    blocks: list[Block]
    errors: list[dict]
    filename: str = ""

    # -- block lookup -------------------------------------------------
    def top(self, btype: str) -> list[Block]:
        return [b for b in self.blocks if b.type == btype]

    def resources(self, rtype: Optional[str] = None) -> list[Block]:
        out: list[Block] = []
        for b in self.blocks:
            if b.type == "resource" and b.labels:
                if rtype is None or b.labels[0] == rtype:
                    out.append(b)
        return out

    def resource(self, rtype: str) -> Optional[Block]:
        res = self.resources(rtype)
        return res[0] if res else None

    def all_resource_types(self) -> list[str]:
        return sorted({b.labels[0] for b in self.resources() if b.labels})

    def variables(self) -> dict[str, Block]:
        return {b.labels[0]: b for b in self.top("variable") if b.labels}

    def outputs(self) -> dict[str, Block]:
        return {b.labels[0]: b for b in self.top("output") if b.labels}

    def providers(self) -> dict[str, Block]:
        return {b.labels[0]: b for b in self.top("provider") if b.labels}

    def terraform_blocks(self) -> list[Block]:
        return self.top("terraform")

    def locals_map(self) -> dict[str, Attr]:
        out: dict[str, Attr] = {}
        for b in self.top("locals"):
            for a in b.attrs:
                out[a.name] = a
        return out

    def data_sources(self, dtype: Optional[str] = None) -> list[Block]:
        out: list[Block] = []
        for b in self.blocks:
            if b.type == "data" and b.labels:
                if dtype is None or b.labels[0] == dtype:
                    out.append(b)
        return out

    def referenced_variables(self) -> set[str]:
        refs: set[str] = set()
        for fname, src in self.files.items():
            refs.update(re.findall(r"\bvar\.([A-Za-z_][A-Za-z0-9_-]*)", src))
        return refs

    def required_providers(self) -> dict[str, str]:
        out: dict[str, str] = {}
        for tb in self.terraform_blocks():
            for rp in tb.nested("required_providers"):
                for a in rp.attrs:
                    out[a.name] = a.raw
        return out


def parse_files(files: dict[str, str]) -> Config:
    all_blocks: list[Block] = []
    errors: list[dict] = []

    for fname, src in files.items():
        toks, lex_errors = tokenize(src)
        for ln, msg in lex_errors:
            errors.append({"file": fname, "line": ln, "message": msg})
        parser = Parser(src, toks, fname)
        try:
            blocks = parser.parse()
        except Exception as exc:  # pragma: no cover - defensive
            errors.append({"file": fname, "line": 0, "message": str(exc)})
            blocks = []
        for ln, msg in parser.errors:
            errors.append({"file": fname, "line": ln, "message": msg})
        all_blocks.extend(blocks)

    return Config(files=files, blocks=all_blocks, errors=errors)


# ---------------------------------------------------------------------------
# Expression helpers
# ---------------------------------------------------------------------------
def norm(s: Optional[str]) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def unquote(s: Optional[str]) -> Optional[str]:
    s = norm(s)
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"' and "${" not in s:
        try:
            return bytes(s[1:-1], "utf-8").decode("unicode_escape")
        except Exception:
            return s[1:-1]
    return None


def literal(s: Optional[str]):
    s = norm(s)
    u = unquote(s)
    if u is not None:
        return ("string", u)
    if s in ("true", "false"):
        return ("bool", s == "true")
    if re.fullmatch(r"-?\d+", s):
        return ("number", int(s))
    if re.fullmatch(r"-?\d+\.\d+", s):
        return ("number", float(s))
    return (None, s)


def ref_vars(s: Optional[str]) -> set[str]:
    return set(re.findall(r"\bvar\.([A-Za-z_][A-Za-z0-9_-]*)", s or ""))


def has_ref(s: Optional[str], ref: str) -> bool:
    if not s:
        return False
    pattern = r"(?<![\w.])" + re.escape(ref)
    # A prefix such as "aws_vpc." must be allowed to be followed by a name.
    if ref and (ref[-1].isalnum() or ref[-1] == "_"):
        pattern += r"(?![\w])"
    return re.search(pattern, s) is not None


def tokens_to_raw(toks: list[Token]) -> str:
    parts: list[str] = []
    for t in toks:
        if t.type == "NEWLINE":
            parts.append(" ")
        elif t.type == "STRING":
            parts.append('"' + t.value + '"')
        elif t.type == "HEREDOC":
            parts.append(t.value)
        else:
            parts.append(t.value)
    return norm("".join(parts))


def object_map(attr: Optional[Attr]) -> Optional[dict[str, str]]:
    """Parse a `{ key = value, ... }` object expression into raw values."""
    if not attr:
        return None
    toks = attr.tokens
    i = 0
    while i < len(toks) and toks[i].type == "NEWLINE":
        i += 1
    if i >= len(toks) or toks[i].type != "LBRACE":
        return None
    i += 1
    items: dict[str, str] = {}
    while i < len(toks):
        t = toks[i]
        if t.type in ("NEWLINE", "COMMA"):
            i += 1
            continue
        if t.type == "RBRACE":
            break
        if t.type in ("IDENT", "STRING"):
            key = t.value
            i += 1
            while i < len(toks) and toks[i].type == "NEWLINE":
                i += 1
            if i < len(toks) and toks[i].type in ("EQUALS", "COLON"):
                i += 1
                vstart = i
                vdepth = 0
                while i < len(toks):
                    tt = toks[i]
                    if tt.type in ("LBRACE", "LBRACK", "LPAREN"):
                        vdepth += 1
                    elif tt.type in ("RBRACE", "RBRACK", "RPAREN"):
                        if vdepth == 0:
                            break
                        vdepth -= 1
                    elif vdepth == 0 and tt.type in ("NEWLINE", "COMMA"):
                        break
                    i += 1
                val = toks[vstart:i]
                if val:
                    items[key] = tokens_to_raw(val)
                continue
        i += 1
    return items


def list_strings(attr: Optional[Attr]) -> list[str]:
    """Best-effort extraction of string literals from a list expression."""
    if not attr:
        return []
    return [t.value for t in attr.tokens if t.type == "STRING"]
