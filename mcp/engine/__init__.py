from typing import Any, Dict, Optional

class MCPEngine:

    def __init__(self):
        pass

    def model(self, model: str):
        from ..model import MCPModel
        return MCPModel(self, model)
