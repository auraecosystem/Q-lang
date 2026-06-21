from q_core import QEngine
from q_parser import QParser

class QRuntime:
    def __init__(self):
        self.engine = QEngine()
        self.parser = QParser()

    def execute(self, script: str):
        ast = self.parser.parse(script)

        results = []

        for node in ast:

            if node[0] == "detect":
                results.append(self.engine.detector.detect(node[1]))

            elif node[0] == "analyze":
                results.append(self.engine.understand(node[1]))

            elif node[0] == "run":
                results.append(self.engine.run(node[1]))

            elif node[0] == "define":
                results.append({"define": node})

        return results
