# Q-lang Execution

Q-lang is executable through the Python runtime while the language surface continues to evolve.

## Run a program

```bash
python q_cli.py examples/hello.q
```

After installation:

```bash
pip install -e .
q examples/hello.q
```

## Semantic lifecycle

Q programs can express the semantic pipeline:

```q
detect "examples/hello.q"
analyze "Q-lang"
infer "Q-lang"
classify "Q-lang"
register "Q-lang"
learn "Q-lang"
coordinate "inspect repository"
run "Q-lang"
verify "Q-lang"
```

The runtime delegates semantic state to `Core.QEngine` and agent coordination to the Agent bridge. External tool execution remains behind the agent/MCP boundary.

## Architecture

```text
Q source
   |
   v
Lexer -> Parser -> AST
                 |
                 v
             Q Runtime
              /     \
       Semantic Core  Agent Bridge
              |          |
          Registry     MCP/Agents
              \          /
               LMLM / Web4
```

## CI

Every push and pull request compiles the runtime, executes the Python tests, and runs the hello-world Q program.
