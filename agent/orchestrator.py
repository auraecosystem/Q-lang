import sys
import json
from ai_eng_core import AIEngineAgent

def main():
    # Enforce basic CLI arguments criteria
    if len(sys.argv) < 3:
        print("Usage: python orchestrator.py <AgentIdentifier> '<TargetObjectiveJSON>'", file=sys.stderr)
        sys.exit(1)
        
    agent_name = sys.argv[1]
    raw_payload = sys.argv[2]
    
    try:
        parsed_objective = json.loads(raw_payload)
    except json.JSONDecodeError:
        print("[-] Critical: Passed payload parameter must be valid structural JSON.", file=sys.stderr)
        sys.exit(1)
        
    # Spin up the agent entity inside the runtime loop
    agent = AIEngineAgent(agent_id=agent_name)
    
    # Simulate routing a dummy semantic target definition to map parameters
    target_object_mock = {
        "name": parsed_objective.get("target_name", "DefaultDataNode"),
        "type": parsed_objective.get("target_type", "Database"),
        "metadata": parsed_objective.get("metadata", {})
    }
    
    agent.map_semantic_context(target_object_mock)
    execution_result = agent.run_cycle(objective=parsed_objective.get("action", "verify"))
    
    # Return output as clear, structured JSON string for the parser to intercept
    print(json.dumps(execution_result, indent=2))

if __name__ == "__main__":
    main()
