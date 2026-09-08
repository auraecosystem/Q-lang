# Q-lang Protocol

The runtime exposes a deterministic orchestration pipeline:

`ROUTE → INSTRUCT → VERIFY → RESULT`

`ROUTE` selects the target agent from execution context. `INSTRUCT` delegates the action through the Agent bridge when available. `VERIFY` accepts only a successful/accepted/completed protocol response. `RESULT` seals the operation with the action, target, instruction response, verification record, and timestamp.

The protocol is intentionally transport-neutral. MCP, LMLM, Web4 services, or another execution adapter can be connected through the instructor callback without making the Q runtime itself responsible for arbitrary network or tool execution.
