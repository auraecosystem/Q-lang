"""Executable Q-lang runtime."""
import sys
from pathlib import Path
from Parser.q_parser import QParser, QSyntaxError
from Core.q_core import QEngine
from Protocol.q_protocol import QProtocol, ProtocolError

try:
    from Agent.q_bridge import QAgentBridge
except ImportError:
    QAgentBridge = None


class QReturn(Exception):
    def __init__(self, value): self.value = value


class QRuntime:
    """Tree-walking VM for Q-lang with semantic orchestration."""
    def __init__(self, agent=None):
        self.parser = QParser()
        self.engine = QEngine()
        self.env = {}
        self.functions = {}
        self.max_loop_iterations = 100000
        self.agent_bridge = agent or (QAgentBridge() if QAgentBridge else None)
        instructor = self._agent_instruct if self.agent_bridge else None
        self.protocol = QProtocol(instructor=instructor)

    def execute(self, source: str):
        results = []
        for node in self.parser.parse(source):
            value = self._eval(node)
            if value is not None: results.append(value)
        return results

    def _eval(self, node):
        kind = node[0]
        if kind == "literal": return node[1]
        if kind == "name": return self.env.get(node[1], node[1])
        if kind in ("let", "assign"):
            value = self._eval(node[2]); self.env[node[1]] = value; return value
        if kind == "list": return [self._eval(x) for x in node[1]]
        if kind == "unary":
            value = self._eval(node[2]); return not value if node[1] == "!" else -value
        if kind == "binop": return self._binop(node[1], node[2], node[3])
        if kind == "fn":
            self.functions[node[1]] = (node[2], node[3]); return {"function": node[1]}
        if kind == "return": raise QReturn(self._eval(node[1]))
        if kind == "if": return self._eval_block(node[2] if self._eval(node[1]) else node[3])
        if kind == "while":
            result = None; count = 0
            while self._eval(node[1]):
                count += 1
                if count > self.max_loop_iterations: raise RuntimeError("while loop exceeded safety iteration limit")
                result = self._eval_block(node[2])
            return result
        if kind == "define":
            return self.engine.registry.register(node[2], node[1], body=node[3])
        if kind in ("detect", "understand", "analyze", "infer", "classify", "register", "learn", "coordinate", "run", "verify"):
            return self._semantic(kind, self._eval(node[1]))
        if kind == "call": return self._call(node[1], [self._eval(x) for x in node[2]])
        if kind == "expr": return self._eval(node[1])
        raise RuntimeError(f"Unknown Q AST node: {kind}")

    def _eval_block(self, body):
        result = None
        for statement in body: result = self._eval(statement)
        return result

    def _binop(self, op, left, right):
        a = self._eval(left)
        if op == "&&" and not a: return False
        if op == "||" and a: return True
        b = self._eval(right)
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "/": return a / b
        if op == "==": return a == b
        if op == "!=": return a != b
        if op == "<": return a < b
        if op == ">": return a > b
        if op == "<=": return a <= b
        if op == ">=": return a >= b
        if op == "&&": return bool(a and b)
        if op == "||": return bool(a or b)
        raise RuntimeError(f"Unknown operator: {op}")

    def _agent_instruct(self, action, context):
        return self.agent_bridge.instruct(action, context)

    def _semantic(self, operation, value):
        if operation == "detect": return self.engine.detector.detect(value)
        if operation in ("understand", "analyze"): return self.engine.understand(value)
        if operation == "infer": return {"inference": "unknown", "object": value}
        if operation == "classify": return {"object": value, "class": type(value).__name__}
        if operation == "register": return self.engine.registry.register(str(value), type(value).__name__)
        if operation == "learn": return {"learned": True, "object": value}
        if operation == "coordinate":
            return self.protocol.execute(str(value), {"runtime": "q-lang"})
        if operation == "run": return self.engine.run(value)
        if operation == "verify": return self.engine.verify(value)
        raise RuntimeError(f"Unknown semantic operation: {operation}")

    def _call(self, name, args):
        if name == "print": print(*args); return args[-1] if args else None
        if name == "len": return len(args[0])
        if name == "type": return type(args[0]).__name__
        if name not in self.functions: raise RuntimeError(f"Unknown function: {name}")
        params, body = self.functions[name]
        if len(params) != len(args): raise RuntimeError(f"{name} expects {len(params)} arguments")
        old = self.env.copy(); self.env.update(zip(params, args)); result = None
        try:
            for statement in body: result = self._eval(statement)
        except QReturn as ret:
            result = ret.value
        finally:
            self.env = old
        return result


def run_file(path):
    return QRuntime().execute(Path(path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m Runtime.q_runtime <file.q>"); raise SystemExit(2)
    try:
        print(run_file(sys.argv[1]))
    except (QSyntaxError, RuntimeError, ProtocolError, QReturn) as exc:
        print(f"Q-lang error: {exc}", file=sys.stderr); raise SystemExit(1)
