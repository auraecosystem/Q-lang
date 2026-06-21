# q_parser.py

class QParser:

    def parse(self, text: str):
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        commands = []

        for line in lines:
            if line.startswith("detect"):
                commands.append(("detect", line.split(" ")[1]))

            elif line.startswith("analyze"):
                commands.append(("analyze", line.split(" ")[1]))

            elif line.startswith("learn"):
                commands.append(("learn", line.split(" ")[1]))

            elif line.startswith("run"):
                commands.append(("run", line.split(" ")[1]))

        return commands
