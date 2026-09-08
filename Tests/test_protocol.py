import unittest

from Protocol.q_protocol import QProtocol, ProtocolError


class TestQProtocol(unittest.TestCase):
    def test_complete_pipeline(self):
        calls = []

        def instructor(action, context):
            calls.append((action, context["stage"]))
            return {"status": "success", "action_executed": action}

        protocol = QProtocol(instructor)
        result = protocol.execute("build Web4 agent", {"agent": "lamis"})

        self.assertEqual([event.operation for event in protocol.events], ["ROUTE", "INSTRUCT", "VERIFY", "RESULT"])
        self.assertEqual(calls, [("build Web4 agent", "INSTRUCT")])
        self.assertEqual(result["status"], "completed")
        self.assertTrue(result["verification"]["verified"])

    def test_verify_rejects_failure(self):
        protocol = QProtocol(lambda action, context: {"status": "failed"})
        with self.assertRaises(ProtocolError):
            protocol.execute("unsafe action")
        self.assertEqual([event.operation for event in protocol.events], ["ROUTE", "INSTRUCT", "VERIFY"])


if __name__ == "__main__":
    unittest.main()
