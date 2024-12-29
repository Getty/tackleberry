from typing import Any, Union, Dict, List, Optional
import os

from . import TBEngine

class TBEngineAnthropic(TBEngine):
    default_max_tokens = 256

    def __init__(self,
        api_key: str = None,
        max_tokens: int = None,
        **kwargs,
    ):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not isinstance(self.api_key, str) or len(self.api_key) < 51:
            raise Exception("Anthropic needs api_key (ANTHROPIC_API_KEY)")
        from anthropic import Anthropic
        self.client = Anthropic(
            api_key=self.api_key,
            **kwargs,
        )
        self.max_tokens = max_tokens or TBEngineAnthropic.default_max_tokens

    def get_models(self):
        models = []
        for model in self.client.models.list().data:
            models.append(model.id)
        models.sort()
        return models

    def __str__(self):
        return f"TB Engine Anthropic {hex(id(self))}"
