class TBEngine:

    def __init__(self):
        pass

    def model(self, model: str):
        from ..model import TBModel
        return TBModel(self, model)

    def chat(self, model: str):
        from ..model import TBModelChat
        return TBModelChat(self, model)
