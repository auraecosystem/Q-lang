"""Q-lang parser for the Universal Semantic Language."""
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

_TOKEN = re.compile(r'(?P<WS>[ \t\r\n]+)|(?P<COMMENT>//[^\n]*)|(?P<STRING>"(?:\\.|[^"\\])*")|(?P<NUMBER>\d+(?:\.\d+)?)|(?P<ID>[A-Za-z_][A-Za-z0-9_]*)|(?P<OP>==|!=|<=|>=|&&|\|\||::|[=+\-*/<>!(),{}\[\]:])')

class QParser:
    def tokenize(self, source: str) -> List[Token]:
        out, pos, line, col = [], 0, 1, 1
        while pos < len(source):
            m = _TOKEN.match(source, pos)
            if not m:
                raise QSyntaxError(f"Unexpected character at {line}:{col}: {source[pos]!r}")
            text, kind = m.group(0), m.lastgroup
            if kind not in ("WS", "COMMENT"):
                out.append(Token(kind, text, line, col))
            nls = text.count("\n")
            if nls:
                line, col = line + nls, len(text.rsplit("\n", 1)[-1]) + 1
            else:
                col += len(text)
            pos = m.end()
        out.append(Token("EOF", "", line, col))
        return out

    def parse(self, source: str) -> List[Any]:
        self.tokens, self.i = self.tokenize(source), 0
        nodes = []
        while not self._check("EOF"):
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
            body = self.block()
            return ("fn", name, args, body)
        if self._match("ID", "return"):
            return ("return", self.expression())
        if self._match("ID", "if"):
            condition = self.expression()
            then_body = self.block()
            else_body = self.block() if self._match("ID", "else") else []
            return ("if", condition, then_body, else_body)
        if self._match("ID", "while"):
            condition = self.expression()
            return ("while", condition, self.block())
        if self._match("ID", "define"):
            target = self._expect("ID").value
            self._expect("OP", "::")
            name = self._expect("STRING").value[1:-1]
            body = self.block() if self._check("OP", "{") else []
            return ("define", target, name, body)
        for keyword in ("detect", "understand", "analyze", "infer", "classify", "register", "learn", "coordinate", "run", "verify"):
            if self._match("ID", keyword):
                return (keyword, self.expression())
        return ("expr", self.expression())

    def block(self):
        self._expect("OP", "{")
        body = []
        while not self._check("OP", "}"):
            if self._check("EOF"):
                raise QSyntaxError("Unclosed block")
            body.append(self.statement())
        self._expect("OP", "}")
        return body

    def expression(self):
        return self.assignment()

    def assignment(self):
        left = self.logical_or()
        if self._match("OP", "="):
            if left[0] != "name":
                raise QSyntaxError("Assignment target must be an identifier")
            return ("assign", left[1], self.assignment())
        return left

    def logical_or(self):
        left = self.logical_and()
        while self._match("OP", "||"):
            left = ("binop", "||", left, self.logical_and())
        return left

    def logical_and(self):
        left = self.equality()
        while self._match("OP", "&&"):
            left = ("binop", "&&", left, self.equality())
        return left

    def equality(self):
        left = self.comparison()
        while self._check("OP", "==") or self._check("OP", "!="):
            op = self._advance().value
            left = ("binop", op, left, self.comparison())
        return left

    def comparison(self):
        left = self.term()
        while self._check("OP", "<") or self._check("OP", ">") or self._check("OP", "<=") or self._check("OP", ">="):
            op = self._advance().value
            left = ("binop", op, left, self.term())
        return left

    def term(self):
        left = self.factor()
        while self._check("OP", "+") or self._check("OP", "-"):
            op = self._advance().value
            left = ("binop", op, left, self.factor())
        return left

    def factor(self):
        left = self.unary()
        while self._check("OP", "*") or self._check("OP", "/"):
            op = self._advance().value
            left = ("binop", op, left, self.unary())
        return left

    def unary(self):
        if self._match("OP", "!"):
            return ("unary", "!", self.unary())
        if self._match("OP", "-"):
            return ("unary", "-", self.unary())
        return self.primary()

    def primary(self):
        if self._match("STRING"):
            raw = self.previous().value[1:-1]
            return ("literal", bytes(raw, "utf-8").decode("unicode_escape"))
        if self._match("NUMBER"):
            v = self.previous().value
            return ("literal", float(v) if "." in v else int(v))
        if self._match("ID", "true"): return ("literal", True)
        if self._match("ID", "false"): return ("literal", False)
        if self._match("ID", "null"): return ("literal", None)
        if self._match("OP", "["):
            values = []
            if not self._check("OP", "]"):
                values.append(self.expression())
                while self._match("OP", ","): values.append(self.expression())
            self._expect("OP", "]")
            return ("list", values)
        if self._match("ID"):
            name = self.previous().value
            if self._match("OP", "("):
                args = []
                if not self._check("OP", ")"):
                    args.append(self.expression())
                    while self._match("OP", ","): args.append(self.expression())
                self._expect("OP", ")")
                return ("call", name, args)
            return ("name", name)
        if self._match("OP", "("):
            x = self.expression(); self._expect("OP", ")"); return x
        t = self.peek()
        raise QSyntaxError(f"Expected expression at {t.line}:{t.column}")

    def _match(self, k, v=None):
        if self._check(k, v): self.i += 1; return True
        return False
    def _check(self, k, v=None):
        t = self.peek(); return t.kind == k and (v is None or t.value == v)
    def _expect(self, k, v=None):
        if not self._check(k, v):
            t = self.peek(); raise QSyntaxError(f"Expected {v or k} at {t.line}:{t.column}")
        return self._advance()
    def _advance(self):
        t = self.tokens[self.i]; self.i += 1; return t
    def peek(self): return self.tokens[self.i]
    def previous(self): return self.tokens[self.i - 1]
