// Define a local service object
define Service::"CustomerDB" {
    type: "PostgreSQL",
    endpoint: "localhost:1111"
}

// Define an AI model that interacts with tools via the Model Context Protocol (MCP)
define Agent::"Analyst" {
    model: "lmlmodel",
    protocol: "McpRegistry"
}

// Chain execution using the Universal Form
understand CustomerDB * coordinate Analyst * run Analyst
