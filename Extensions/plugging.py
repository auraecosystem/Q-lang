class QPluginSystem:
    def __init__(self):
        self.plugins = {}

    def register(self, ext, handler):
        self.plugins[ext] = handler

    def execute(self, ext, data):
        if ext in self.plugins:
            return self.plugins[ext](data)
        return None
