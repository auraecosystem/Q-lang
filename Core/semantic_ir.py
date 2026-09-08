"""Canonical Semantic IR for Q-lang directives.

The IR deliberately does not depend on Unicode surface syntax.  Parsers may
map ^↑D, ^↓D, ^→D and ^←D to the same internal representation.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VerificationContract:
    postconditions: List[str] = field(default_factory=list)
    evidence_required: bool = True


@dataclass
class SemanticIR:
    intent: str
    subject: Any
    operator: str = "DEEP_SEMANTIC"
    direction: str = "UP"
    mode: str = "deep"
    depth: Optional[int] = None
    perspective: Optional[str] = None
    entities: List[Dict[str, Any]] = field(default_factory=list)
    concepts: List[str] = field(default_factory=list)
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    operations: List[str] = field(default_factory=list)
    execution_plan: List[Dict[str, Any]] = field(default_factory=list)
    verification: VerificationContract = field(default_factory=VerificationContract)
    confidence: float = 0.0
    provenance: Dict[str, Any] = field(default_factory=dict)
    status: str = "semantic"

    def to_dict(self) -> Dict[str, Any]:
        value = dict(self.__dict__)
        value["verification"] = dict(self.verification.__dict__)
        return value
