import unittest

from Core.q_directive_parser import DirectiveParser
from Engine.semantic_runtime import SemanticRuntime


class SemanticDirectiveTests(unittest.TestCase):
    def test_parse_up_directive(self):
        directive = DirectiveParser().parse("^↑D Explain neural-symbolic compilation")
        self.assertEqual(directive.operator, "DEEP_SEMANTIC")
        self.assertEqual(directive.direction, "UP")
        self.assertFalse(directive.execution)

    def test_semantic_phase_produces_ir(self):
        result = SemanticRuntime().run("^↑D Explain neural-symbolic compilation")
        self.assertEqual(result["phase"], "SEMANTIC")
        self.assertEqual(result["ir"]["operator"], "DEEP_SEMANTIC")
        self.assertIn("neural-symbolic", result["ir"]["concepts"])

    def test_execute_verify_result_learn(self):
        runtime = SemanticRuntime()
        result = runtime.run("^↑D create a Next.js application ^D")
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["verification"]["verified"])
        self.assertEqual(runtime.state["last_result"]["status"], "success")
        self.assertTrue(any(x.get("status") == "verified" for x in runtime.processor.knowledge))


if __name__ == "__main__":
    unittest.main()
