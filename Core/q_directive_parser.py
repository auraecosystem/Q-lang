"""Small, dependency-free parser for Q-lang semantic directives."""
import re
from .directives import Directive


class DirectiveParser:
    _pattern = re.compile(r"^\s*\^(?P<direction>[↑↓→←])D\s+(?P<subject>.+?)(?:\s+\^D)?\s*$")

    def parse(self, source: str) -> Directive:
        match = self._pattern.match(source)
        if not match:
            raise SyntaxError("Invalid Q directive. Expected: ^↑D <subject> [^D]")
        direction = {"↑": "UP", "↓": "DOWN", "→": "FORWARD", "←": "REVERSE"}[match.group("direction")]
        subject = match.group("subject").strip()
        execution = source.rstrip().endswith("^D")
        if execution:
            subject = re.sub(r"\s+\^D\s*$", "", subject).strip()
        return Directive(
            operator="DEEP_SEMANTIC" if direction == "UP" else "SEMANTIC_DIRECTION",
            direction=direction,
            subject=subject,
            execution=execution,
        )
