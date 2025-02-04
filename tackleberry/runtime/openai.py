import os

from .base import TBRuntime
from ..context import TBContext
from ..chat import TBChat

from openai import OpenAI

from pydantic import BaseModel

class TBRuntimeOpenai(TBRuntime):

    def __init__(self,
        api_key: str = None,
        temperature: float = None,
        **kwargs,
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not isinstance(self.api_key, str) or len(self.api_key) < 51:
            raise Exception("OpenAI needs api_key (OPENAI_API_KEY)")
        # TODO vvv see comment on ollama.py
        if not temperature is None:
            self.temperature = temperature
        # TODO ^^^
        self.client = OpenAI(
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
        chat_kwargs = {
            "model": chat.model.name,
            "messages": self.get_messages_from_context(context),
        }
        if struct is not None:
            response = self.client.beta.chat.completions.parse(
                **chat_kwargs,
                response_format=struct,
            )
            print(response);
            return response.choices[0].message.parsed
        else:
            response = self.client.chat.completions.create(
                **chat_kwargs,
            )
            return response.choices[0].message.content

    def __str__(self):
        return f"TB Runtime OpenAI {hex(id(self))}"
