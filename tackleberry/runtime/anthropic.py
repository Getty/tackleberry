import os

from .base import TBRuntime
from ..context import TBContext
from ..chat import TBChat

import instructor
from pydantic import BaseModel

class TBRuntimeAnthropic(TBRuntime):
    default_max_tokens = 512

    def __init__(self,
        api_key: str = None,
        max_tokens: int = None,
        **kwargs,
    ):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not isinstance(self.api_key, str) or len(self.api_key) < 51:
            raise Exception(str(self)+" needs api_key (ANTHROPIC_API_KEY)")
        from anthropic import Anthropic
        self.client = Anthropic(
            api_key=self.api_key,
            **kwargs,
        )
        self.max_tokens = max_tokens or TBRuntimeAnthropic.default_max_tokens

    def get_models(self):
        models = []
        for model in self.client.models.list().data:
            models.append(model.id)
        models.sort()
        return models

    def chat_context(self, chat: TBChat, context: TBContext, struct: BaseModel = None, **kwargs):
        if struct is not None:
            client = instructor.from_anthropic(self.client)
            response = client.messages.create(
                model=chat.model.name,
                max_tokens=self.max_tokens,
                messages=self.get_messages_from_context(context),
                response_model=struct,
            )
            return response
        else:
            response = self.client.messages.create(
                model=chat.model.name,
                max_tokens=self.max_tokens,
                messages=self.get_messages_from_context(context),
            )
            return response.content

    def __str__(self):
        return f"TB Runtime Anthropic {hex(id(self))}"
