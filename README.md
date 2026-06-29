# Q-lang (Universal Semantic Language)

Q is a semantic computing language designed to understand, define, analyze, learn, coordinate, and execute any digital or conceptual object. Unlike traditional programming languages that focus exclusively on compiling logical operations into specific machine code instructions, Q focuses entirely on mapping and orchestrating
**meaning**.
In the Q ecosystem, **everything is treated as an Object**—whether it is a raw file, a legacy script, an AI model, a communication protocol, a decentralized blockchain ledger, or a human-defined conceptual framework.


## 🚀 Core Principles1. 

**Everything is an Object.** 
Any piece of data, code, or model can be wrapped.2.
**Everything has Meaning.** 
Entities are mapped by their logical context and capabilities.3. **Everything can be Analyzed & Defined.** 
Unknown elements are broken down automatically.4. 
**Everything can be Learned.**
Once ingested, objects are indexed for future programs.5. 
**Everything can be Coordinated & Executed.** 
Objects seamlessly interact across technical stacks.

## 🛠️ Repository Architecture
The project codebase relies primarily on **Ruby** and **Python**, split across specialized directory layers designed to parse and evaluate semantic syntax:
```bash
├── Q_cli/           # Command Line Interface execution binaries
├── Core/            # Core processing engine of the language environment
├── Engine/          # Runtime execution state manager
├── Parser/          # Abstract syntax tree (AST) interpreter for .q / .pq files
├── Runtime/         # Live context execution machine
├── Learning_loop/   # Continuous reinforcement layer for discovered objects
├── Agent/           # Built-in autonomous AI worker integrations
├── Blockchain/      # Decentralized cryptographic ledger connectors
├── Extensions/      # Web hooks, plugins, and third-party bindings
└── example/         # Implementation templates and boilerplate configurations
```
## 🔄 Universal Form Syntax
All evaluations inside Q-lang flow through a linear operation chain known as the **Universal Form**:
```q
understand * define * analyze * learn * coordinate * run
```
*Where `*` acts as a placeholder representing any known or unknown system object.*

### A Complete Pipeline Example 
(`Program.pq`)
```q
// Define a local service object
define Service::"CustomerDB" {
    type: "PostgreSQL",
    endpoint: "localhost:5432"
}

// Define an AI model that interacts with tools via the Model Context Protocol (MCP)
define Agent::"Analyst" {
    model: "Claude-3.5-Sonnet",
    protocol: "McpRegistry"
}

// Chain execution using the Universal Form
understand CustomerDB * coordinate Analyst * run Analyst
```
---
## 🧬 Unknown Object Lifecycle
When the execution runtime encounters an unmapped file type or data stream, it safely loops it through an automated discovery cycle instead of throwing an exception:


[ Volatile Input ] ──> detect ──> analyze ──> infer ──> classify ──> register ──> learn ──> [ Active Ecosystem ]


1. **`detect unknown`**: Flags the black-box item inside the physical workspace.
2. **`analyze unknown`**: Performs parsing checks on internal structural patterns.
3. **`infer unknown`**: Contextually determines the operational intent and constraints.
4. **`classify unknown`**: Assigns a definitive system type (e.g., protocol, script, dataset).
5. **`register unknown`**: Locks a recognizable instance signature into the workspace environment.
6. **`learn unknown`**: Incorporates features into the active database, making it fully available to all future program chains.

```q
// Discovery scripting example
detect unknown::"etc/analytics.rbx"
analyze unknown
classify unknown as "DataTransformer"
learn DataTransformer
```

---

## 💻 Technical Stack

The code distribution consists of the following primary development languages and tool frameworks:
* **Ruby (56.7%)**: Drives the main compiler logic, setup tasks, and core automation frameworks.
* **Python (18.2%)**: Drives AI agent tools, data science integrations, and internal model handlers.
* **Shell (10.2%)**: Local environment setup tools and automated terminal processes.
* **q / OverPy / Power Query (14.9%)**: Native evaluation syntax, analytical data querying parsers, and custom typing files.

---

## 🤝 Contributing

Contributions are welcome! Please review our core guidelines before opening a pull request:
1. Ensure new operational bindings extend the native components in `/Core`.
2. Provide an abstract mapping template in the `/example` directory for any newly supported services.
3. All syntax adjustments must successfully map through the internal validation check in `/Parser`.

## 📄 License

This project is open-source and maintained under the [Aura Ecosystem](https://github.com)

 "Aura Ecosystem Organization Hub") organizational guidelines.



cd Q-lang
gem install bundler && bundle install
pip install -r requirements.txt
```

### 2. Verification
```bash
./Q_cli/bin/q-lang check example/Program.pq
```

---

## 🔄 Universal Form & MCP Integration

Objects are managed via the **Universal Form** (`understand * define * analyze * learn * coordinate * run`).

The `Agent/` directory uses the **Model Context Protocol (MCP)** to map external tools/data for AI agents.

```q
// Define and coordinate a secure agent
define Agent::"SecurityGuard" { model: "Claude-3.5-Sonnet", protocol: "McpRegistry" }
coordinate Agent::"SecurityGuard" { target: SystemScanner }
run SecurityGuard
```

---

## 🧬 Unknown Object Lifecycle
When encountering unknown objects, the system automatically runs a discovery cycle: `detect` -> `analyze` -> `infer` -> `classify` -> `register` -> `learn`.

---

## 💻 Technical Stack
*   **Ruby (56.7%)**: Core Engine & CLI.
*   **Python (18.2%)**: Learning loop & Agents.
*   **Shell (10.2%)**: Bootstrapping.
*   **Q/PQ (14.9%)**: Syntax.

---

## 📄 License
Maintained under [Aura Ecosystem](https://github.com) guidelines.

