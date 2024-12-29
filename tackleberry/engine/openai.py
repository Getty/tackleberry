from typing import Any, Union, Dict, List, Optional
import os

from . import TBEngine

class TBEngineOpenai(TBEngine):

    def __init__(self,
        api_key: str = None,
        **kwargs,
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not isinstance(self.api_key, str) or len(self.api_key) < 51:
            raise Exception("OpenAI needs api_key (OPENAI_API_KEY)")
        from openai import OpenAI
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

    def __str__(self):
        return f"TB Engine OpenAI {hex(id(self))}"
