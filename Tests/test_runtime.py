"""Smoke tests for the Q-lang MVP runtime."""
import unittest
from Parser.q_parser import QParser
from Runtime.q_runtime import QRuntime

class QLangTests(unittest.TestCase):
    def test_expression_precedence(self):
        self.assertEqual(QRuntime().execute('let x = 2 + 3 * 4'), [14])

    def test_control_flow(self):
        source = '''
        let x = 0
        while x < 3 {
            x = x + 1
        }
        if x == 3 { print("ok") }
        '''
        self.assertEqual(QRuntime().execute(source)[-1], "ok")

    def test_function_return(self):
        source = '''
        fn add(a, b) { return a + b }
        add(2, 5)
        '''
        self.assertEqual(QRuntime().execute(source)[-1], 7)

    def test_semantic_operations(self):
        results = QRuntime().execute('detect "Web4"\nclassify "Web4"\nverify "Web4"')
        self.assertEqual(results[0]["detected_type"], "symbolic")
        self.assertEqual(results[1]["class"], "str")
        self.assertTrue(results[2]["verified"])

if __name__ == "__main__":
    unittest.main()
