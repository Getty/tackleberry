import os

from .base import TBRuntime
from ..context import TBContext
from ..chat import TBChat

from anthropic import Anthropic

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
            text_blocks = []
            for content in response.content:
                text_blocks.append(self.content_to_text(content))
            return '\n\n'.join(filter(None, text_blocks))

    def content_to_text(self, content):
        if content.type == 'text':
            return content.text

        elif content.type == 'code':
            return f"```{content.language or ''}\n{content.text}\n```"

        elif hasattr(content, 'text') and content.text:
            return "["+content.type+"] "+content.text

    def __str__(self):
        return f"TB Runtime Anthropic {hex(id(self))}"
