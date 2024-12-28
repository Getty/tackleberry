from typing import Any, Union, Dict, List, Optional
import uuid
import yaml
import os

from .engine import MCPEngine

class MCPRegistry:

    def __init__(self, name: Optional[str] = None):
        if name is None:
            name = str(uuid.uuid4())
        current_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.normpath(os.path.join(current_dir, 'registry.yaml'))
        with open(yaml_path, 'r') as file:
            self._engine_models = yaml.safe_load(file)
        self._loaded_engines = {}
        self._update_models()

    def _update_models(self):
        self._models = {}
        for engine in self._engine_models:
            for model in self._engine_models[engine]:
                self._models[model] = engine

    def get_engine_by_model(self, model: str):
        return self._models[model]

    def add_engine(self, name: str, engine: MCPEngine = None):
        self._engines[name] = engine
        return self._engines[name]

    def __str__(self):
        return f"MCP Registry {self.name}"
