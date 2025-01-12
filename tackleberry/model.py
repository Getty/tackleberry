from .runtime import TBRuntime

class TBModel:

    def __init__(self, runtime: TBRuntime, name: str, **kwargs):
        self.runtime = runtime
        self.name = name
        self.options = kwargs

    def chat(self, **kwargs):
        from .chat import TBChat
        return TBChat(self, **kwargs)
