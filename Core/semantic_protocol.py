"""Executable semantic protocol for Q-lang.

^D Create builds an execution envelope without performing the side effect.
^D Validate is a deterministic gate between INSTRUCT and EXECUTE.
The runtime protocol is ROUTE -> INSTRUCT -> VALIDATE -> EXECUTE -> VERIFY -> RESULT.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class SemanticRequest:
    intent: str
    subject: Any
    direction: str = "UP"
    operations: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    verification: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    phase: str
    errors: List[str] = field(default_factory=list)
    checks: Dict[str, bool] = field(default_factory=dict)


@dataclass(frozen=True)
class SemanticExecution:
    request: SemanticRequest
    route: Dict[str, Any]
    instruction: Dict[str, Any]
    validation: ValidationResult


def create_execution(ir, route: Dict[str, Any]) -> SemanticExecution:
    """Create an execution envelope; creation has no side effects."""
    request = SemanticRequest(
        intent=ir.intent,
        subject=ir.subject,
        direction=ir.direction,
        operations=list(ir.operations),
        capabilities=list(ir.capabilities),
        constraints=list(ir.constraints),
        verification={
            "postconditions": list(ir.verification.postconditions),
            "evidence_required": ir.verification.evidence_required,
        },
    )
    instruction = {
        "capability": route.get("capability"),
        "intent": request.intent,
        "subject": request.subject,
        "operations": request.operations,
    }
    validation = validate_execution(request, route, instruction)
    return SemanticExecution(request, route, instruction, validation)


def validate_execution(
    request: SemanticRequest,
    route: Dict[str, Any],
    instruction: Dict[str, Any],
) -> ValidationResult:
    """Validate the complete execution envelope before any side effect."""
    errors: List[str] = []
    checks = {
        "intent": bool(request.intent),
        "subject": request.subject is not None,
        "route": bool(route.get("capability")),
        "instruction": instruction.get("intent") == request.intent,
        "capability": instruction.get("capability") == route.get("capability"),
    }
    for name, passed in checks.items():
        if not passed:
            errors.append(f"validation failed: {name}")

    if request.capabilities and route.get("capability") not in request.capabilities:
        errors.append("validation failed: routed capability is not requested")
        checks["requested_capability"] = False
    else:
        checks["requested_capability"] = True

    return ValidationResult(
        valid=not errors,
        phase="VALIDATED" if not errors else "REJECTED",
        errors=errors,
        checks=checks,
    )
