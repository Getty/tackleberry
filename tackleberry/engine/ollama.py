from typing import Any, Union, Dict, List, Optional
import os
from urllib.parse import urlparse
import base64

from . import TBEngine

class TBEngineOllama(TBEngine):

    def __init__(self,
        url: str = None,
        **kwargs,
    ):
        url = os.environ.get("OLLAMA_HOST")
        userinfo = None
        if os.environ.get("OLLAMA_PROXY_URL"):
            if not url is None:
                raise Exception("OLLAMA_PROXY_URL and OLLAMA_HOST set, please just use one")
            else:
                url = os.environ.get("OLLAMA_PROXY_URL")
        if url:
            parsed_url = urlparse(os.environ.get("OLLAMA_HOST"))
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
                url = 'http://'+parsed_url.path+'/'
            kwargs['host'] = url
        if userinfo:
            if not 'headers' in kwargs:
                kwargs['headers'] = {}
            auth_bytes = userinfo.encode("utf-8")
            auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
            kwargs['headers']['Authorization'] = 'Basic '+auth_base64
        from ollama import Client as Ollama
        self.client = Ollama(
            **kwargs,
        )

    def get_models(self):
        models = []
        for model in self.client.list().models:
            models.append(model.model)
        models.sort()
        return models

    def __str__(self):
        return f"TB Engine Ollama {hex(id(self))}"
