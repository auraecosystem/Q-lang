import unittest

from Parser.q_parser import QParser
from Runtime.q_runtime import QRuntime
from Core.q_directive_parser import DirectiveParser


class SemanticDirectiveTests(unittest.TestCase):
    def test_parse_up_directive(self):
        directive = DirectiveParser().parse("^↑D Explain neural-symbolic compilation")
        self.assertEqual(directive.operator, "DEEP_SEMANTIC")
        self.assertEqual(directive.direction, "UP")
        self.assertFalse(directive.execution)

    def test_semantic_phase_produces_ir(self):
        result = QRuntime().execute("^↑D Explain neural-symbolic compilation")[0]
        self.assertEqual(result["phase"], "SEMANTIC")
        self.assertEqual(result["ir"]["operator"], "DEEP_SEMANTIC")
        self.assertIn("neural-symbolic", result["ir"]["concepts"])

    def test_execution_is_simulated_without_adapter(self):
        runtime = QRuntime()
        result = runtime.execute("^↑D create a Next.js application ^D")[0]

        self.assertEqual(result["status"], "simulated")
        self.assertFalse(result["observation"]["executed"])
        self.assertFalse(result["verification"]["verified"])
        self.assertEqual(runtime.state["last_result"]["status"], "simulated")
        self.assertFalse(any(x.get("status") == "verified" for x in runtime.semantic.knowledge))

    def test_adapter_requires_explicit_verification_and_evidence(self):
        runtime = QRuntime(
            executor=lambda instruction: {
                "verified": True,
                "evidence": {"postcondition": "resource_exists"},
            }
        )
        result = runtime.execute("^↑D create a test resource ^D")[0]

        self.assertEqual(result["status"], "verified")
        self.assertTrue(result["verification"]["verified"])
        self.assertTrue(any(x.get("status") == "verified" for x in runtime.semantic.knowledge))

    def test_adapter_without_evidence_is_not_trusted(self):
        runtime = QRuntime(executor=lambda instruction: {"verified": True, "evidence": {}})
        result = runtime.execute("^↑D create a test resource ^D")[0]

        self.assertEqual(result["status"], "unverified")
        self.assertFalse(result["verification"]["verified"])
        self.assertFalse(any(x.get("status") == "verified" for x in runtime.semantic.knowledge))

    def test_existing_q_parser_remains_available(self):
        nodes = QParser().parse("let x = 2 + 3")
        self.assertEqual(nodes[0][0], "let")


if __name__ == "__main__":
    unittest.main()
