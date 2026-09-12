import unittest

from Core.semantic_protocol import create_execution, validate_execution
from Core.semantic_ir import SemanticIR
from Engine.semantic_runtime import SemanticRuntime


class SemanticProtocolTests(unittest.TestCase):
    def test_create_does_not_execute(self):
        calls = []
        runtime = SemanticRuntime(executor=lambda instruction: calls.append(instruction))
        ir = SemanticIR(intent="EXECUTE", subject="create object")
        execution = create_execution(ir, runtime.route(ir))
        self.assertTrue(execution.validation.valid)
        self.assertEqual(calls, [])

    def test_invalid_capability_is_rejected(self):
        ir = SemanticIR(intent="EXECUTE", subject="create object", capabilities=["q.required"])
        result = validate_execution(
            request=__import__("Core.semantic_protocol", fromlist=["SemanticRequest"]).SemanticRequest(
                intent=ir.intent,
                subject=ir.subject,
                capabilities=ir.capabilities,
            ),
            route={"capability": "q.other"},
            instruction={"capability": "q.other", "intent": ir.intent, "subject": ir.subject},
        )
        self.assertFalse(result.valid)
        self.assertIn("routed capability is not requested", " ".join(result.errors))

    def test_runtime_executes_only_after_validation(self):
        seen = []
        runtime = SemanticRuntime(executor=lambda instruction: seen.append(instruction) or {"ok": True})
        result = runtime.run("^↑D create object ^D")
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(seen), 1)
        self.assertTrue(result["validation"]["valid"])


if __name__ == "__main__":
    unittest.main()
