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

_TOKEN = re.compile(r'(?P<WS>[ \t\r\n]+)|(?P<COMMENT>//[^\n]*)|(?P<STRING>"(?:\\.|[^"\\])*")|(?P<NUMBER>\d+(?:\.\d+)?)|(?P<ID>[A-Za-z_][A-Za-z0-9_]*)|(?P<OP>==|!=|<=|>=|::|[=+*(),{}])')

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
            if nls: line, col = line + nls, len(text.rsplit("\n", 1)[-1]) + 1
            else: col += len(text)
            pos = m.end()
        out.append(Token("EOF", "", line, col)); return out

    def parse(self, source: str) -> List[Any]:
        self.tokens, self.i = self.tokenize(source), 0
        nodes = []
        while not self._check("EOF"): nodes.append(self.statement())
        return nodes

    def statement(self):
        if self._match("ID", "let"):
            name = self._expect("ID").value; self._expect("OP", "=")
            return ("let", name, self.expression())
        if self._match("ID", "fn"):
            name = self._expect("ID").value; self._expect("OP", "("); args=[]
            if not self._check("OP", ")"):
                args.append(self._expect("ID").value)
                while self._match("OP", ","): args.append(self._expect("ID").value)
            self._expect("OP", ")"); self._expect("OP", "{"); body=[]
            while not self._check("OP", "}"): body.append(self.statement())
            self._expect("OP", "}"); return ("fn", name, args, body)
        if self._match("ID", "return"): return ("return", self.expression())
        if self._match("ID", "define"):
            target=self._expect("ID").value; self._expect("OP", "::"); name=self._expect("STRING").value[1:-1]
            if self._match("OP", "{"):
                depth=1
                while depth:
                    if self._match("OP", "{"): depth += 1
                    elif self._match("OP", "}"): depth -= 1
                    elif self._check("EOF"): raise QSyntaxError("Unclosed define block")
                    else: self._advance()
            return ("define", target, name)
        for keyword in ("detect", "analyze", "run", "verify"):
            if self._match("ID", keyword): return (keyword, self.expression())
        return ("expr", self.expression())

    def expression(self):
        left=self.primary()
        if self._match("OP", "="):
            if left[0] != "name": raise QSyntaxError("Assignment target must be an identifier")
            return ("assign", left[1], self.expression())
        while self._check("OP", "+") or self._check("OP", "*"):
            op=self._advance().value; left=("binop", op, left, self.primary())
        return left

    def primary(self):
        if self._match("STRING"):
            raw=self.previous().value[1:-1]; return ("literal", bytes(raw,"utf-8").decode("unicode_escape"))
        if self._match("NUMBER"):
            v=self.previous().value; return ("literal", float(v) if "." in v else int(v))
        if self._match("ID"):
            name=self.previous().value
            if self._match("OP", "("):
                args=[]
                if not self._check("OP", ")"):
                    args.append(self.expression())
                    while self._match("OP", ","): args.append(self.expression())
                self._expect("OP", ")"); return ("call", name, args)
            return ("name", name)
        if self._match("OP", "("):
            x=self.expression(); self._expect("OP", ")"); return x
        t=self.peek(); raise QSyntaxError(f"Expected expression at {t.line}:{t.column}")

    def _match(self,k,v=None):
        if self._check(k,v): self.i+=1; return True
        return False
    def _check(self,k,v=None):
        t=self.peek(); return t.kind==k and (v is None or t.value==v)
    def _expect(self,k,v=None):
        if not self._check(k,v):
            t=self.peek(); raise QSyntaxError(f"Expected {v or k} at {t.line}:{t.column}")
        return self._advance()
    def _advance(self): t=self.tokens[self.i]; self.i+=1; return t
    def peek(self): return self.tokens[self.i]
    def previous(self): return self.tokens[self.i-1]
