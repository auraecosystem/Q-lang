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

    def test_execute_verify_result_learn(self):
        runtime = QRuntime()
        result = runtime.execute("^↑D create a Next.js application ^D")[0]
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["verification"]["verified"])
        self.assertEqual(runtime.state["last_result"]["status"], "success")
        self.assertTrue(any(x.get("status") == "verified" for x in runtime.semantic.knowledge))

    def test_existing_q_parser_remains_available(self):
        nodes = QParser().parse('let x = 2 + 3')
        self.assertEqual(nodes[0][0], "let")


if __name__ == "__main__":
    unittest.main()
