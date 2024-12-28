from typing import Any, Union, Dict, List, Optional
from openai import OpenAI
import os

from . import MCPEngine

class MCPEngineOpenai(MCPEngine):

    def __init__(self,
        api_key: str = None,
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not isinstance(self.api_key, str) or len(self.api_key) < 51:
            raise Exception("OpenAI needs api_key (OPENAI_API_KEY)")
        self.client = OpenAI(api_key=self.api_key)

    def update_models(self):
        self.models = []
        for model in self.client.models.list().data:
            models.append(model.id)
        self.models.sort()

    def __str__(self):
        return f"MCP Engine OpenAI {hex(id(self))}"
