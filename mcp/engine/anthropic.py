from typing import Any, Union, Dict, List, Optional
import os

from . import MCPEngine

class MCPEngineAnthropic(MCPEngine):
    default_max_tokens = 256

    def __init__(self,
        api_key: str = None,
        max_tokens: int = None,
    ):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not isinstance(self.api_key, str) or len(self.api_key) < 51:
            raise Exception("Anthropic needs api_key (ANTHROPIC_API_KEY)")
        from anthropic import Anthropic
        self.client = Anthropic(api_key=self.api_key)
        self.max_tokens = max_tokens or MCPEngineAnthropic.default_max_tokens

    def update_models(self):
        self.models = []
        for model in self.client.models.list().data:
            self.models.append(model.id)
        self.models.sort()

    def __str__(self):
        return f"MCP Engine Anthropic {hex(id(self))}"
