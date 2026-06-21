# cli.py

from q_runtime import QEngine

engine = QEngine()

print("Q Runtime Active")

# Example usage
result = engine.understand("./test.py")

print(result)
