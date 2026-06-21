# q_parser.py
class QParser:

    def parse(self, text):
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        ast = []

        for l in lines:

            if l.startswith("detect"):
                ast.append(("detect", l.split(" ")[1]))

            elif l.startswith("analyze"):
                ast.append(("analyze", l.split(" ")[1]))

            elif l.startswith("learn"):
                ast.append(("learn", l.split(" ")[1]))

            elif l.startswith("run"):
                ast.append(("run", l.split(" ")[1]))

            elif ":" in l:
                key, value = l.split(":", 1)
                ast.append(("define", key.strip(), value.strip()))

        return ast
