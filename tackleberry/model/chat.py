from typing import Union

from .base import TBModel
from ..engine import TBEngine
from ..context import TBContext, TBSystemPromptError

class TBModelChat(TBModel):

    def __init__(self,
        engine: TBEngine,
        model_name_or_model: Union[str, TBModel],
        context: TBContext = None,
        system_prompt: str = None,
        **kwargs,
    ):
        self.engine = engine
        if context is not None and system_prompt is not None:
            raise TBSystemPromptError("A TBModelChat can't handle system_prompt and context at once.")
        self.system_prompt = system_prompt
        self.context = context
        if isinstance(model_name_or_model, TBModel):
            self.model = model_name_or_model
        else:
            self.model = self.engine.model(model_name_or_model)
        self.name = model_name_or_model.name
