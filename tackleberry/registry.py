from typing import Any, Union, Dict, List, Optional
import uuid
import yaml
import os

from .runtime import TBRuntime

class TBRegistry:

    def __init__(self, name: Optional[str] = None):
        if name is None:
            name = str(uuid.uuid4())
        self._runtimes = {}
        self._update_models()

    def load_registry(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.normpath(os.path.join(current_dir, 'registry.yaml'))
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)

    def _update_models(self):
        self._models = {}
        registry = self.load_registry()
        for runtime_name in self._runtimes:
            # If the runtime is in registry, then we delete it from there to not collide with the specific version
            if runtime_name in registry:
                del registry[runtime_name]
            hasattr(self._runtimes[runtime_name], 'get_models')
            for model in self._runtimes[runtime_name].get_models:
                self._models[model] = runtime_name
        for registry_runtime in registry:
            for model in registry[registry_runtime]:
                self._models[model] = registry_runtime

    def get_runtime_by_model(self, model: str):
        return self._models[model]

    def add_runtime(self, name: str, runtime: TBRuntime = None):
        self._runtimes[name] = runtime
        self._update_models()
        return self

    def __str__(self):
        return f"TB Registry {self.name}"
