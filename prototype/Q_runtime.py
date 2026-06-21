# q_runtime.py

import os
import re
from pathlib import Path


class QObject:
    def __init__(self, path):
        self.path = path
        self.type = None
        self.language = None
        self.metadata = {}

    def __repr__(self):
        return f"<QObject type={self.type} language={self.language} path={self.path}>"


class QDetector:
    """
    Detect file types + map to semantic language
    """

    RULES = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".rs": "rust",
        ".go": "golang",
        ".sol": "solidity",
        ".md": "markdown",
        ".json": "data",
    }

    def detect(self, path: str):
        ext = Path(path).suffix
        obj = QObject(path)

        obj.language = self.RULES.get(ext, "unknown")

        if obj.language == "unknown":
            obj.type = "unknown"
        else:
            obj.type = "source"

        return obj


class QAnalyzer:
    """
    Basic static analysis layer (expandable into AI layer later)
    """

    def analyze(self, qobj: QObject):
        if qobj.language == "python":
            return self._analyze_python(qobj.path)

        if qobj.language == "javascript":
            return self._analyze_js(qobj.path)

        return {"status": "no analyzer available"}

    def _analyze_python(self, path):
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        imports = re.findall(r"^import .*|^from .* import .*", code, re.M)
        functions = re.findall(r"def (.*)\(", code)

        return {
            "imports": imports,
            "functions": functions,
        }

    def _analyze_js(self, path):
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        imports = re.findall(r"import .* from .*", code)
        functions = re.findall(r"function (.*?)\(", code)

        return {
            "imports": imports,
            "functions": functions,
        }


class QExecutor:
    """
    Execution layer (safe stub for now)
    """

    def run(self, qobj: QObject):
        if qobj.language == "python":
            os.system(f"python {qobj.path}")

        elif qobj.language == "javascript":
            os.system(f"node {qobj.path}")

        else:
            return "No runtime available"


class QEngine:
    """
    Full semantic pipeline:
    detect → analyze → execute
    """

    def __init__(self):
        self.detector = QDetector()
        self.analyzer = QAnalyzer()
        self.executor = QExecutor()

    def understand(self, path):
        obj = self.detector.detect(path)
        analysis = self.analyzer.analyze(obj)

        return {
            "object": repr(obj),
            "analysis": analysis
        }

    def run(self, path):
        obj = self.detector.detect(path)
        return self.executor.run(obj)
