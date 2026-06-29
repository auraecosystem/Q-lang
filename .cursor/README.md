

# Q-lang (Universal Semantic Language)
Q is a semantic computing language designed to understand, define, analyze, learn, coordinate, and execute any digital or conceptual object. Unlike traditional programming languages that focus exclusively on compiling logical operations into machine instructions, Q maps and orchestrates **meaning**.

In the Q ecosystem, **everything is treated as an Object**—whether it is a file, a legacy script, an AI model, a communication protocol, a decentralized blockchain ledger, or an abstract conceptual framework.
---## 🚀 Core Principles1.  **Everything is an Object.** Wrap code, datasets, and models into uniform semantic entities.2.  **Everything has Meaning.** Entities are mapped and understood by their logical intent and operational boundaries.3.  **Everything can be Analyzed & Defined.** Unknown or black-box components are broken down dynamically.4.  **Everything can be Learned.** Once ingested, objects are permanently indexed for future program cycles.5.  **Everything can be Coordinated & Executed.** Native asset orchestration bridges diverse tech stacks.
---## 🛠️ Repository Architecture
The project codebase relies primarily on a hybrid Ruby and Python architecture:
*   `Core/` & `Parser/`: Core compiler engine, AST parsing logic, and language validation rules.
*   `Engine/` & `Runtime/`: Active state manager and live evaluation context environment.
*   `Agent/`: Subsystems facilitating autonomous AI worker integrations and tool bindings.
*   `Blockchain/`: Cryptographic layer connectors for decentralized state management.
*   `Learning_loop/`: Reinforcement engine providing continuous optimization for discovered objects.
*   `Q_cli/`: Local command-line interfaces, shell bindings, and executable binaries.

---## 📦 Installation & Local Setup### PrerequisitesEnsure you have Ruby (`3.2.0+`), Python (`3.10.0+`), Bundler, and `pip` installed globally on your machine.

### 1. Environment DeploymentClone the repository and install dependencies for both the core parser and the agent processing stacks:
```bash
git clone 
https://github.com
cd Q-lang
gem install bundler && bundle install
pip install -r requirements.txt```
ʼʼʼ
```
### 2. Verify Installation
Run a localized syntax verification pass using the command-line execution framework:

```bash
./Q_cli/bin/q-lang check example/Program.pq```
```
---

## ⚙️ Configuration & Environment Variables

Copy the distributed environment template into your active runtime root directory:
```bash
cp .env.example .env```
```
Configure the following essential environment keys to enable autonomous execution loops:

| Variable Name | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `QLANG_ENV` | No | `development` | Defines the engine runtime environment mode (`development`, `production`). |
| `ANTHROPIC_API_KEY` | Yes (for Agents)| `None` | Authentication key enabling semantic model evaluations in `Agent/`. |
| `MCP_REGISTRY_PATH` | No | `~/.mcp/registry`| Custom localized path containing valid Model Context Protocol tool schemas. |
| `BLOCKCHAIN_PROVIDER` | No | `http://127.0.0.1:8545`| Remote RPC link managing live smart contract state mappings. |

---

## 🔄 Universal Form & MCP Integration

All operations inside Q-lang execute through a chained pipeline layout termed the **Universal Form**:

```q
understand * define * analyze * learn * coordinate * run```
*Where `*` acts as an active placeholder representing any mapped system object.*

The `Agent/` ecosystem natively adopts the **Model Context Protocol (MCP)** via its internal registry system. This design configuration allows AI agents to scan, interpret, and invoke software utilities safely in a sandbox without structural source code edits:

```q
// Define a local service object
define Service::"CustomerDatabase" {
    type: "PostgreSQL",
    endpoint: "localhost:5432"
}

// Instantiate an AI agent wired to use MCP tools
define Agent::"SecurityScanner" {
    model: "Claude-3.5-Sonnet",
    protocol: "McpRegistry"
}

// Chain execution across layers via the Universal Form syntax
understand CustomerDatabase * coordinate SecurityScanner * run SecurityScanner
```

---

## 🧬 Unknown Object Lifecycle

If the engine meets unmapped file formats or third-party raw scripts, it kicks off an automated discovery pipeline to avoid system faults:


[ Volatile Input ] ──> detect ──> analyze ──> infer ──> classify ──> register ──> learn ──> [ Active Ecosystem ]


1.  **`detect unknown`**: Targets an unidentified file/stream inside the active runtime workspace.
2.  **`analyze unknown`**: Evaluates syntax structures and maps base layout features.
3.  **`infer unknown`**: Contextually tracks object intent, requirements, and call targets.
4.  **`classify unknown`**: Assigns a precise semantic identity tag (e.g., protocol, application script).
5.  **`register unknown`**: Locks a unique identification stamp for the object instance inside the session.
6.  **`learn unknown`**: Incorporates features permanently into the active workspace ecosystem.

---

## 💻 Technical Stack

*   **Ruby (56.7%)**: Powers the primary parser mechanics, AST rules, and local CLI tools.
*   **Python (18.2%)**: Runs the continuous learning loops and agent orchestrations.
*   **Shell (10.2%)**: System initialization tools and shell hooks.
*   **q / OverPy / Power Query (14.9%)**: Target syntax scripts and analytical querying logic.

---

## 🤖 CI/CD Automation (`.github/workflows/q-validate.yml`)

This project uses an automated GitHub Actions pipeline to validate files on every pull request. Save this configuration block to check your code layout:

```yaml
name: Q-Lang Semantic Validator

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code Repository
        uses: actions/checkout@v4

      - name: Setup Ruby Runtime
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundle-cache: true

      - name: Validate Project Syntax Maps
        run: |
          ./Q_cli/bin/q-lang check example/Program.pq
          ./Q_cli/bin/q-lang check __init__.q
```

---

## 🤝 Contributing

Contributions are welcome! Please ensure any modifications to compiler syntax or core logic successfully clear validation within the `/Parser` test suite prior to submitting a pull request.

## 📄 License

Maintained under the [Aura Ecosystem](https://github.com)

) open-source development 
---------



