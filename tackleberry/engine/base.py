class TBEngine:

    def __init__(self):
        pass

    def model(self,
        model: str,
        **kwargs,
    ):
        from ..model import TBModel
        return TBModel(self, model, **kwargs)

    def chat(self,
        model: str,
        **kwargs,
    ):
        from ..model import TBModelChat
        return TBModelChat(self, model, **kwargs)
