from typing import Union

from .context import TBContext
from .model import TBModel

from pydantic import BaseModel

class TBChat:
    count = 0

    def __init__(self,
        model_name_or_model: Union[str, TBModel],
        context: TBContext = None,
        system_prompt: str = None,
        struct: BaseModel = None,
        name: str = None,
        **kwargs,
    ):
        TBChat.count += 1
        self.name = name or f'TBChat-{TBChat.count}'
        if isinstance(model_name_or_model, TBModel):
            self.model = model_name_or_model
        else:
            from . import TB
            self.model = TB.model(model_name_or_model)
        self.struct = struct
        self.context = context if context is not None else TBContext()
        if system_prompt is not None:
            self.context.add_system(system_prompt)
        self.model_name = self.model.name
        self.runtime = self.model.runtime

    def get_messages(self):
        return self.runtime.get_messages_from_context(self.context)

    def query(self,
        query_or_context: Union[str, TBContext],
        struct: BaseModel = None,
        **kwargs,
    ):
        context = query_or_context if isinstance(query_or_context, TBContext) else self.context.copy_with_query(query_or_context)
        return self.runtime.chat_context(self, context, struct=struct, **kwargs)
