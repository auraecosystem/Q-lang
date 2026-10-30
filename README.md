# Q-lang — Universal Semantic Language

Q-lang is an experimental semantic language and runtime for expressing meaning-oriented operations over data, code, services, and conceptual objects. Its goal is to connect semantic interpretation with explicit, verifiable execution rather than treating every input as an ordinary expression.

> **Project status:** early-stage research and MVP runtime. The Python interpreter and its tests are the current executable baseline. Several directories contain prototypes or experiments; their presence does not imply production-ready compiler, agent, blockchain, or multi-language support.

## Design goals

- **Object-oriented semantic representation:** describe entities together with their context, properties, relationships, and capabilities.
- **Semantic processing:** explore a pipeline of detection, analysis, inference, classification, registration, and learning.
- **Explicit coordination:** represent delegated work through a route/instruct/verify/result protocol.
- **Execution boundaries:** separate semantic interpretation from actions that may affect external systems.
- **Verification-gated learning:** treat observed evidence and verified outcomes as prerequisites for trusted knowledge.

These are design goals. The current implementation only partially realizes them; see [Implementation status](Docs/IMPLEMENTATION_STATUS.md).

## Semantic directive notation

The directive parser currently recognizes these operator families:

| Form | Current parser meaning |
| --- | --- |
| `^↑D` | Deep semantic processing in the upward direction |
| `^↓D` | Semantic processing in the downward direction |
| `^→D` | Semantic processing in the forward direction |
| `^←D` | Semantic processing in the reverse direction |
| `^D` suffix | Marks a directive as an execution request |

Examples:

```text
^↑D Explain neural-symbolic compilation
^↑D create a Q-lang project ^D
```

The first form requests semantic interpretation. The second requests the runtime's current execution path. At this stage, execution is a **simulation**, not a general-purpose operating-system or external-service executor. A successful simulated response must not be interpreted as proof that a real-world action occurred.

## Architecture map

| Area | Responsibility in the current codebase |
| --- | --- |
| `Parser/` | Q source lexer/parser and syntax errors |
| `Core/` | Core engine, directive parsing, semantic IR and processing |
| `Runtime/` | Python tree-walking interpreter and directive entry point |
| `Protocol/` | ROUTE → INSTRUCT → VERIFY → RESULT protocol |
| `Agent/` | Agent bridge and experimental agent integration |
| `Engine/` | Additional semantic-runtime experiment; not yet consolidated with `Runtime/` |
| `Learning_loop/` | Learning experiments; not yet a trusted persistent learning system |
| `Tests/` | Python unittest suite for parser, runtime, directives and protocol |
| `src/`, `main.rs`, language-specific folders | Experimental language/compiler work; not the active Python runtime |

There are currently overlapping semantic-runtime implementations. The ordinary Q interpreter is in `Runtime/q_runtime.py`; semantic directive orchestration is also implemented there. The separate `Engine/` runtime and the protocol/agent abstractions are not yet a single unified execution path.

## Requirements

- Python 3.10 or newer
- Git (to clone the repository)

The current Python test suite uses the standard library `unittest`; no third-party Python test dependency is required.

## Quick start

Clone and enter the repository:

```bash
git clone https://github.com/auraecosystem/Q-lang.git
cd Q-lang
python -m Runtime.q_runtime path/to/program.q
```

Run a Q source file through the installed-style CLI module:

```bash
python q_cli.py path/to/program.q
```

The CLI prints each non-null result returned by the runtime. The `q` console entry point is declared in `pyproject.toml`; install the project in editable mode if you want to use that entry point:

```bash
python -m pip install -e .
q path/to/program.q
```

## Run tests

From the repository root:

```bash
python -m compileall -q Core Parser Runtime Protocol Agent q_cli.py
python -m unittest discover -s Tests -p "test_*.py" -v
```

The same checks are run by `bash.sh` and the Python GitHub Actions workflow.

## Runtime safety and current limitations

- Semantic directive execution is dry-run by default: it returns `status: simulated` and `executed: false`. No external action is performed without an explicitly injected executor.
- Programmatic callers may construct `QRuntime(executor=my_executor)`. The executor must return a dictionary containing `verified: true` and non-empty `evidence` before the runtime records a verified result. This is an adapter contract, not independent proof; production use still needs independent postcondition checks.
- Agent adapters are also explicit dependencies. Ordinary local execution does not initialize an agent client or require API credentials.
- The semantic inference implementation is heuristic and should not be treated as a calibrated model or confidence score.
- Agent/MCP-related code is experimental; the repository does not yet provide a production-ready, permissioned MCP tool execution environment.
- Persistent learning, rollback, authorization policy, capability isolation, and independently verified postconditions require further implementation.
- The Python runtime, the additional Engine runtime, and experimental Rust/other-language artifacts have not yet been consolidated into one compiler/runtime contract.

Do not connect this runtime to production systems or grant it sensitive credentials until authorization, sandboxing, audit logging, and independent verification have been implemented and reviewed.

## Development direction

The recommended sequence is:

1. Establish the Python implementation as the reference runtime and keep CI green.
2. Define the language grammar, AST, directive semantics, and Semantic IR contract.
3. Consolidate semantic execution so there is one authoritative coordinator.
4. Route agent delegation through the protocol rather than bypassing it.
5. Replace simulated execution with explicit capability adapters, authorization, and sandbox boundaries.
6. Verify real postconditions using independent evidence; only then promote knowledge to trusted state.
7. Add persistence, rollback, compatibility tests, packaging, and release documentation.
8. Reintroduce other language implementations behind conformance tests once the language contract is stable.

## Contributing

1. Preserve existing parser and runtime behavior unless a change is covered by tests.
2. Add or update tests for every behavior change.
3. Keep simulated behavior clearly labeled; never report a simulated action as a real execution.
4. Document experimental components and known limitations.
5. Run the complete test command before submitting a pull request.

## License

See the repository's license file for the applicable terms.
