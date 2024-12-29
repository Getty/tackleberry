from typing import Any, Union, Dict, List, Optional
import os

from . import TBEngine

class TBEngineGroq(TBEngine):

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

    def __str__(self):
        return f"TB Engine Groq {hex(id(self))}"
