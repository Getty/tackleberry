import os

from .base import TBRuntime
from ..context import TBContext
from ..chat import TBChat

from mistralai import Mistral

import instructor
from pydantic import BaseModel

class TBRuntimeMistral(TBRuntime):
    default_max_tokens = 512

    def __init__(self,
        api_key: str = None,
        max_tokens: int = None,
        temperature: float = None,
        **kwargs,
    ):
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        if not isinstance(self.api_key, str) or len(self.api_key) < 32:
            raise Exception("MistralAI needs api_key (MISTRAL_API_KEY)")
        # TODO vvv see comment on ollama.py
        if not temperature is None:
            self.temperature = temperature
        # TODO ^^^
        self.client = Mistral(
            api_key=self.api_key,
            **kwargs,
        )
        self.max_tokens = max_tokens or TBRuntimeMistral.default_max_tokens

    def get_models(self):
        models = []
        for model in self.client.models.list().data:
            models.append(model.id)
        models.sort()
        return models

    def chat_context(self, chat: TBChat, context: TBContext, struct: BaseModel = None, **kwargs):
        chat_kwargs = {
            "model": chat.model.name,
            "messages": self.get_messages_from_context(context),
        }
        if struct is not None:
            client = instructor.from_mistral(
                client=self.client,
                model=chat.model.name,
                mode=instructor.Mode.MISTRAL_TOOLS,
                max_tokens=self.max_tokens,
            )
            del chat_kwargs["model"]
            response = client.messages.create(
                **chat_kwargs,
                response_model=struct,
            )
            return response
        else:
            response = self.client.chat.complete(
                **chat_kwargs,
            )
            return response.choices[0].message.content

    def __str__(self):
        return f"TB Runtime MistralAI {hex(id(self))}"
