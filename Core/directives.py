"""Canonical Q-lang directive semantics.

^↑D performs semantic acquisition; ^D is the execution directive.  The
semantic pipeline is explicit and deterministic at the orchestration layer:
DETECT -> ANALYZE -> INFER -> CLASSIFY -> REGISTER -> LEARN -> SYNTHESIZE.
"""
from dataclasses import dataclass
from typing import Any, Dict, List

from .semantic_ir import SemanticIR, VerificationContract


@dataclass(frozen=True)
class Directive:
    operator: str
    direction: str
    subject: Any
    mode: str = "deep"
    depth: int | None = None
    perspective: str | None = None
    execution: bool = False


class DeepSemanticProcessor:
    """Build SemanticIR without executing side effects."""

    def __init__(self, registry=None):
        self.registry = registry
        self.knowledge: List[Dict[str, Any]] = []

    def detect(self, subject: Any) -> Dict[str, Any]:
        if isinstance(subject, str):
            kind = "text"
        elif isinstance(subject, dict):
            kind = "mapping"
        elif isinstance(subject, (list, tuple)):
            kind = "sequence"
        else:
            kind = type(subject).__name__
        return {"type": kind, "subject": subject}

    def analyze(self, subject: Any, detected: Dict[str, Any]) -> Dict[str, Any]:
        text = subject if isinstance(subject, str) else repr(subject)
        return {"text": text, "tokens": text.split(), "detected": detected}

    def infer(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        tokens = analysis["tokens"]
        return {"intent": "EXECUTE" if "create" in [t.lower() for t in tokens] else "UNDERSTAND",
                "dependencies": [], "inferred_operations": []}

    def classify(self, analysis: Dict[str, Any], inference: Dict[str, Any]) -> Dict[str, Any]:
        return {"domain": "general", "intent": inference["intent"], "language": "natural"}

    def register(self, ir_data: Dict[str, Any]) -> Dict[str, Any]:
        if self.registry is not None:
            self.registry.register(str(ir_data["subject"]), "semantic_subject", intent=ir_data["intent"])
        return {"registered": True}

    def learn(self, ir_data: Dict[str, Any]) -> Dict[str, Any]:
        # Learning is only provisional here. Trusted learning occurs after VERIFY.
        record = {"intent": ir_data["intent"], "status": "provisional"}
        self.knowledge.append(record)
        return record

    def synthesize(self, directive: Directive) -> SemanticIR:
        detected = self.detect(directive.subject)
        analysis = self.analyze(directive.subject, detected)
        inference = self.infer(analysis)
        classification = self.classify(analysis, inference)
        data = {
            "subject": directive.subject,
            "intent": inference["intent"],
        }
        registration = self.register(data)
        learning = self.learn(data)
        return SemanticIR(
            intent=inference["intent"],
            subject=directive.subject,
            direction=directive.direction,
            mode=directive.mode,
            depth=directive.depth,
            perspective=directive.perspective,
            concepts=analysis["tokens"],
            dependencies=inference["dependencies"],
            operations=inference["inferred_operations"],
            capabilities=[],
            verification=VerificationContract(),
            confidence=1.0 if analysis["tokens"] else 0.0,
            provenance={"detected": detected, "classification": classification,
                        "registration": registration, "learning": learning},
        )
