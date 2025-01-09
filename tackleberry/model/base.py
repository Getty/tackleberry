from ..engine import TBEngine

class TBModel:

    def __init__(self, engine: TBEngine, name: str):
        self.engine = engine
        self.name = name

    def chat(self, **kwargs):
        from .chat import TBModelChat
        return TBModelChat(self.engine, self, **kwargs)
