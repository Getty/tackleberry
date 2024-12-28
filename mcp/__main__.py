from typing import Any, Dict, Optional
from importlib import import_module

from .registry import MCPRegistry
from .engine import MCPEngine

class MCPMain:
    count = 0
    registry = MCPRegistry('__main__')

    def __init__(self,
        name: Optional[str] = None,
        registry: Optional[MCPRegistry] = None,
    ):
        MCPMain.count += 1
        self.name = name or f'MCP-{MCPMain.count}'
        self.registry = registry if registry else MCPMain.registry
        self.engines = {}

    def __str__(self):
        return f"MCPMain instance {self.name}"

    def model(self,
        model: str,
        **kwargs,
    ):
        model_parts = model.split('/')
        if len(model_parts) > 1:
            engine_class = model_parts.pop(0)
            model = '/'.join(model_parts)
        else:
            engine_class = self.registry.get_engine_by_model(model)
        if engine_class is None:
            raise Exception(f"Can't find engine for model '{model}'")
        engine = self.engine(engine_class, **kwargs)
        if engine is None:
            raise Exception(f"Can't find engine for engine class '{engine_class}'")
        return engine.model(model)

    def engine(self,
        engine_class: str,
        **kwargs,
    ):
        if engine_class in self.engines:
            return self.engines[engine_class]
        try:
            from importlib import import_module
            from_list = [f"MCPEngine{engine_class.title()}"]
            mod = import_module(f".engine.{engine_class}", package=__package__)
            self.engines[engine_class] = getattr(mod, from_list[0])(**kwargs)
        except ImportError:
            mod = import_module(f"mcp.engine.{engine_class}")
            self.engines[engine_class] = getattr(mod, f"MCPEngine{engine_class.title()}")(**kwargs)
        if isinstance(self.engines[engine_class], MCPEngine):
            return self.engines[engine_class]
        else:
            raise Exception(f"Can't find engine '{engine_class}'")

MCP = MCPMain()

__all__ = ['MCP']
