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

## Implemented and tested

- Arithmetic, variables, functions, conditionals, loops, and semantic verbs have runtime tests.
- Directive parsing recognizes the four directional operator forms.
- The protocol tests cover the successful pipeline and rejection of a failed instructor response.
- The protocol records ROUTE, INSTRUCT, VERIFY, and RESULT events without duplicate status arguments.
- Directive execution is **dry-run by default**. Without an explicitly supplied executor, Q-lang returns `status: simulated` and `executed: false`.
- An injected executor must return a dictionary with `verified: true` and non-empty `evidence` before the runtime marks the result verified and adds it to the verified knowledge collection.
- CLI tests cover result output and runtime-error reporting.

## Security boundaries and remaining work

- Dry-run mode does not perform external actions.
- Adapter-provided verification/evidence is a contract boundary, not independent proof. Production use still requires independent postcondition checks and evidence validation.
- The semantic inference path is heuristic, not a trained or calibrated inference engine.
- Agent/MCP integration is not yet a secure general-purpose tool executor.
- Persistent trusted learning, policy enforcement, sandboxing, rollback, and audit-grade evidence are incomplete.
- `Engine/` and `Runtime/` contain overlapping runtime concepts that need consolidation.
- Rust and other language artifacts are experimental and do not yet pass a shared language conformance suite.

Do not connect this runtime to production systems or grant it sensitive credentials until authorization, sandboxing, audit logging, and independent verification have been implemented and reviewed.

## CI contract

The supported CI job compiles the active Python modules and runs:

```bash
python -m unittest discover -s Tests -p "test_*.py" -v
```

Crystal checks are kept as a manually triggered experiment because the repository does not currently define a root `shard.yml` manifest or a Crystal spec suite. Historical Conda, Makefile, and dependency-review workflows are manual-only until their repository prerequisites are configured.
