from typing import Any, Dict, Optional

from ..engine import MCPEngine

class MCPModel:

    def __init__(self, engine: MCPEngine, model: str):
        self.engine = engine
        self.model = model
