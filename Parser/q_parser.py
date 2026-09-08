"""Q-lang parser for the Universal Semantic Language MVP."""
from dataclasses import dataclass
from typing import Any, List
import re


@dataclass
class Token:
    kind: str
    value: str
    line: int
    column: int


class QSyntaxError(ValueError):
    pass


_TOKEN = re.compile(
    r'(?P<WS>[ \t\r\n]+)|(?P<COMMENT>//[^\n]*)|'
    r'(?P<STRING>"(?:\\.|[^"\\])*")|(?P<NUMBER>\d+(?:\.\d+)?)|'
    r'(?P<ID>[A-Za-z_][A-Za-z0-9_:.]*)|(?P<OP>==|!=|<=|>=|[=+*(),{}])'
)


class QParser:
    def tokenize(self, source: str) -> List[Token]:
        out, pos, line, col = [], 0, 1, 1
        while pos < len(source):
            m = _TOKEN.match(source, pos)
            if not m:
                raise QSyntaxError(f"Unexpected character at {line}:{col}: {source[pos]!r}")
            text = m.group(0)
            kind = m.lastgroup
            if kind not in ("WS", "COMMENT"):
                out.append(Token(kind, text, line, col))
            nls = text.count("\n")
            if nls:
                line += nls
                col = len(text.rsplit("\n", 1)[-1]) + 1
            else:
                col += len(text)
            pos = m.end()
        out.append(Token("EOF", "", line, col))
        return out

    def parse(self, source: str) -> List[Any]:
        self.tokens = self.tokenize(source)
        self.i = 0
        nodes = []
        while not self._at("EOF"):
            nodes.append(self.statement())
        return nodes

    def statement(self):
        if self._match("ID", "let"):
            name = self._expect("ID").value
            self._expect("OP", "=")
            return ("let", name, self.expression())
        if self._match("ID", "fn"):
            name = self._expect("ID").value
            self._expect("OP", "(")
            args = []
            if not self._check("OP", ")"):
                args.append(self._expect("ID").value)
                while self._match("OP", ","):
                    args.append(self._expect("ID").value)
            self._expect("OP", ")")
            self._expect("OP", "{")
            body = []
            while not self._check("OP", "}"):
                body.append(self.statement())
            self._expect("OP", "}")
            return ("fn", name, args, body)
        if self._match("ID", "return"):
            return ("return", self.expression())
        if self._match("ID", "define"):
            target = self._expect("ID").value
            name = None
            if self._match("OP", "::"):
                name = self._expect("STRING").value[1:-1]
            return ("define", target, name)
        if self._match("ID", "detect"):
            target = self.expression()
            return ("detect", target)
        if self._match("ID", "analyze"):
            return ("analyze", self.expression())
        if self._match("ID", "run"):
            return ("run", self.expression())
        if self._match("ID", "verify"):
            return ("verify", self.expression())
        return ("expr", self.expression())

    def expression(self):
        left = self.primary()
        while self._check("OP", "+") or self._check("OP", "*"):
            op = self._advance().value
            right = self.primary()
            left = ("binop", op, left, right)
        if self._match("OP", "="):
            if left[0] != "name":
                raise QSyntaxError("Assignment target must be an identifier")
            return ("assign", left[1], self.expression())
        return left

    def primary(self):
        if self._match("STRING"):
            return ("literal", bytes(self.previous().value[1:-1], "utf-8").decode("unicode_escape"))
        if self._match("NUMBER"):
            v = self.previous().value
            return ("literal", float(v) if "." in v else int(v))
        if self._match("ID"):
            name = self.previous().value
            if self._match("OP", "("):
                args = []
                if not self._check("OP", ")"):
                    args.append(self.expression())
                    while self._match("OP", ","):
                        args.append(self.expression())
                self._expect("OP", ")")
                return ("call", name, args)
            return ("name", name)
        if self._match("OP", "("):
            x = self.expression(); self._expect("OP", ")"); return x
        t = self.peek(); raise QSyntaxError(f"Expected expression at {t.line}:{t.column}")

    def _match(self, kind, value=None):
        if self._check(kind, value): self.i += 1; return True
        return False
    def _check(self, kind, value=None):
        t = self.peek(); return t.kind == kind and (value is None or t.value == value)
    def _expect(self, kind, value=None):
        if not self._check(kind, value):
            t = self.peek(); raise QSyntaxError(f"Expected {value or kind} at {t.line}:{t.column}")
        return self._advance()
    def _advance(self):
        t = self.tokens[self.i]; self.i += 1; return t
    def peek(self): return self.tokens[self.i]
    def previous(self): return self.tokens[self.i - 1]
    def _at(self, kind): return self._check(kind)
