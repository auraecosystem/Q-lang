# Q-lang implementation status

This document distinguishes implemented behavior from architecture goals.

## Active executable baseline

The current executable baseline is the Python tree-walking runtime:

- `Parser/` parses the current Q source subset.
- `Core/` provides core semantic structures and directive processing.
- `Runtime/q_runtime.py` evaluates parsed Q programs and handles semantic directives.
- `Protocol/q_protocol.py` provides a separate ROUTE → INSTRUCT → VERIFY → RESULT protocol implementation.
- `Tests/` contains standard-library `unittest` coverage.

The supported Python baseline is 3.10+. CI uses Python 3.11.

## Verified from source inspection

- Arithmetic, variables, functions, conditionals, loops, and semantic verbs have runtime tests.
- Directive parsing recognizes the four directional operator forms.
- The protocol tests cover the successful pipeline and rejection of a failed instructor response.
- The current directive execution path in `Runtime/q_runtime.py` creates a simulated observation and verifies that the observation is non-null.
- The runtime's directive path currently performs its own route/instruct/execute/verify sequence rather than delegating through `QProtocol`.

## Not production-ready

- Simulated execution is not external execution.
- A non-null observation is not sufficient evidence of a real postcondition.
- The semantic inference path is heuristic, not a trained or calibrated inference engine.
- Agent/MCP integration is not yet a secure general-purpose tool executor.
- Persistent trusted learning, policy enforcement, sandboxing, rollback, and audit-grade evidence are incomplete.
- `Engine/` and `Runtime/` contain overlapping runtime concepts that need consolidation.
- Rust and other language artifacts are experimental and do not yet pass a shared language conformance suite.

## CI contract

The supported CI job compiles the active Python modules and runs:

```bash
python -m unittest discover -s Tests -p "test_*.py" -v
```

Crystal checks are kept as a manually triggered experiment because the repository does not currently define a root `shard.yml` manifest or a Crystal spec suite.
