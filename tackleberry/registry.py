from typing import Any, Union, Dict, List, Optional
import uuid
import yaml
import os

from .engine import TBEngine

class TBRegistry:

    def __init__(self, name: Optional[str] = None):
        if name is None:
            name = str(uuid.uuid4())
        self._engines = {}
        self._update_models()

    def load_registry(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.normpath(os.path.join(current_dir, 'registry.yaml'))
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)

    def _update_models(self):
        self._models = {}
        registry = self.load_registry()
        for engine_name in self._engines:
            # If the engine is in registry, then we delete it from there to not collide with the specific version
            if engine_name in registry:
                del registry[engine_name]
            hasattr(self._engines[engine_name], 'get_models')
            for model in self._engines[engine_name].get_models:
                self._models[model] = engine_name
        for registry_engine in registry:
            for model in registry[registry_engine]:
                self._models[model] = registry_engine

    def get_engine_by_model(self, model: str):
        return self._models[model]

    def add_engine(self, name: str, engine: TBEngine = None):
        self._engines[name] = engine
        self._update_models()
        return self

    def __str__(self):
        return f"TB Registry {self.name}"
