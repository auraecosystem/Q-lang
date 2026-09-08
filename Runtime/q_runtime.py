"""Executable Q-lang runtime. Kept separate from the legacy .opy runtime."""
import sys
from pathlib import Path
from Parser.q_parser import QParser, QSyntaxError
from Core.q_core import QEngine

class QRuntime:
    def __init__(self):
        self.parser=QParser(); self.engine=QEngine(); self.env={}; self.functions={}

    def execute(self, source: str):
        results=[]
        for node in self.parser.parse(source):
            value=self._eval(node)
            if value is not None: results.append(value)
        return results

    def _eval(self,node):
        kind=node[0]
        if kind in ("literal",): return node[1]
        if kind=="name":
            if node[1] in self.env: return self.env[node[1]]
            return node[1]
        if kind=="let" or kind=="assign":
            value=self._eval(node[2]); self.env[node[1]]=value; return value
        if kind=="binop":
            a,b=self._eval(node[2]),self._eval(node[3])
            return a+b if node[1]=="+" else a*b
        if kind=="fn": self.functions[node[1]]=(node[2],node[3]); return {"function":node[1]}
        if kind=="return": return self._eval(node[1])
        if kind=="call": return self._call(node[1],[self._eval(x) for x in node[2]])
        if kind=="define": return self.engine.registry.register(node[2],node[1])
        if kind=="detect": return self.engine.detector.detect(self._eval(node[1]))
        if kind=="analyze": return self.engine.understand(self._eval(node[1]))
        if kind=="run": return self.engine.run(self._eval(node[1]))
        if kind=="verify": return self.engine.verify(self._eval(node[1]))
        if kind=="expr": return self._eval(node[1])
        raise RuntimeError(f"Unknown Q AST node: {kind}")

    def _call(self,name,args):
        if name=="print": print(*args); return args[-1] if args else None
        if name not in self.functions: raise RuntimeError(f"Unknown function: {name}")
        params,body=self.functions[name]
        if len(params)!=len(args): raise RuntimeError(f"{name} expects {len(params)} arguments")
        old=self.env.copy(); self.env.update(zip(params,args)); result=None
        for statement in body:
            result=self._eval(statement)
            if statement[0]=="return": break
        self.env=old; return result

def run_file(path):
    return QRuntime().execute(Path(path).read_text(encoding="utf-8"))

if __name__=="__main__":
    if len(sys.argv)!=2:
        print("usage: python -m Runtime.q_runtime <file.q>"); raise SystemExit(2)
    try: print(run_file(sys.argv[1]))
    except (QSyntaxError,RuntimeError) as exc: print(f"Q-lang error: {exc}",file=sys.stderr); raise SystemExit(1)
