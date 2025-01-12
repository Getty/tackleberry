import os

from .base import TBRuntime
from ..context import TBContext
from ..chat import TBChat

import instructor
from pydantic import BaseModel

class TBRuntimeGroq(TBRuntime):

    def __init__(self,
        api_key: str = None,
        **kwargs,
    ):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not isinstance(self.api_key, str) or len(self.api_key) < 51:
            raise Exception("Groq needs api_key (GROQ_API_KEY)")
        from groq import Groq
        self.client = Groq(
            api_key=self.api_key,
            **kwargs,
        )

    def get_models(self):
        models = []
        for model in self.client.models.list().data:
            models.append(model.id)
        models.sort()
        return models

    def chat_context(self, chat: TBChat, context: TBContext, struct: BaseModel = None, **kwargs):
        if struct is not None:
            client = instructor.from_groq(self.client)
            response = client.chat.completions.create(
                model=chat.model.name,
                messages=self.get_messages_from_context(context),
                response_model=struct,
            )
            return response
        else:
            response = self.client.chat.completions.create(
                model=chat.model.name,
                messages=self.get_messages_from_context(context),
            )
            return response.content

    def __str__(self):
        return f"TB Runtime Groq {hex(id(self))}"
