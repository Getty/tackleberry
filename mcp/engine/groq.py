from typing import Any, Union, Dict, List, Optional
from groq import Groq
import os

from . import MCPEngine

class MCPEngineGroq(MCPEngine):

    def __init__(self,
        api_key: str = None,
    ):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not isinstance(self.api_key, str) or len(self.api_key) < 51:
            raise Exception("Groq needs api_key (GROQ_API_KEY)")
        self.client = Groq(api_key=self.api_key)

    def update_models(self):
        self.models = []
        for model in self.client.models.list().data:
            models.append(model.id)
        self.models.sort()

    def __str__(self):
        return f"MCP Engine Groq {hex(id(self))}"
