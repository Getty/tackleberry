from ..context import TBContext

class TBRuntime:

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
        from ..chat import TBChat
        return TBChat(self.model(model), **kwargs)

    def get_messages_from_context(self, context: TBContext):
        return context.to_messages()
