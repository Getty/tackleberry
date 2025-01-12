import os
from urllib.parse import urlparse
import base64

from typing import Union

from .base import TBRuntime
from ..context import TBContext
from ..chat import TBChat

from ollama import Client as Ollama

from pydantic import BaseModel

class TBRuntimeOllama(TBRuntime):

    def __init__(self,
        url: str = None,
        keep_alive: Union[float, str] = None,
        **kwargs,
    ):
        if url is None:
            url = os.environ.get("OLLAMA_HOST")
            userinfo = None
            if os.environ.get("OLLAMA_PROXY_URL"):
                if not url is None:
                    raise Exception("OLLAMA_PROXY_URL and OLLAMA_HOST set, please just use one")
                else:
                    url = os.environ.get("OLLAMA_PROXY_URL")
        parsed_url = urlparse(url)
        if parsed_url.scheme:
            if parsed_url.scheme in ["http", "https"] and parsed_url.netloc:
                if "@" in parsed_url.netloc:
                    userinfo = parsed_url.netloc.split("@")[0]
                    if parsed_url.port:
                        netloc = f"{parsed_url.hostname}:{parsed_url.port}"
                    else:
                        netloc = parsed_url.hostname
                    parsed_url = parsed_url._replace(netloc=netloc)
                url = parsed_url.geturl()
            elif parsed_url.path:
                url = parsed_url.scheme+'://'+parsed_url.path+'/'
            kwargs['host'] = url
        if userinfo:
            if not 'headers' in kwargs:
                kwargs['headers'] = {}
            auth_bytes = userinfo.encode("utf-8")
            auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
            kwargs['headers']['Authorization'] = 'Basic '+auth_base64
        if not keep_alive is None:
            self.keep_alive = keep_alive
        self.client = Ollama(
            **kwargs,
        )

    def get_models(self):
        models = []
        for model in self.client.list().models:
            models.append(model.model)
        models.sort()
        return models

    def chat_context(self, chat: TBChat, context: TBContext, struct: BaseModel = None, **kwargs):
        if struct is not None:
            chat_kwargs = {
                "model": chat.model.name,
                "messages": self.get_messages_from_context(context),
                "format": struct.model_json_schema(),
            }
            if hasattr(self, 'keep_alive'):
                chat_kwargs["keep_alive"] = self.keep_alive
            response = self.client.chat(**chat_kwargs, **kwargs)
            return struct.model_validate_json(response.message.content)
        else:
            response = self.client.chat(
                model=chat.model.name,
                messages=self.get_messages_from_context(context),
                **kwargs,
            )
            return response.message.content

    def __str__(self):
        return f"TB Runtime Ollama {hex(id(self))}"
