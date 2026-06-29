// 1. Define your physical database as a semantic object
define Service::"CustomerDatabase" {
    type: "PostgreSQL",
    location: "localhost:5432",
    context: "Encrypted"
}

// 2. Define an AI Agent capable of interacting with tools via MCP
define Agent::"QueryAssistant" {
    model: "Claude-3.5-Sonnet",
    protocol: "McpRegistry"
}

// 3. Connect them using the Universal Form pipeline
understand CustomerDatabase * coordinate QueryAssistant * run QueryAssistant
