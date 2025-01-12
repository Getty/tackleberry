from typing import Any, Dict, Optional
from importlib import import_module

from .registry import TBRegistry
from .runtime import TBRuntime
from .context import TBContext

class TBMain:
    count = 0
    registry = TBRegistry('__main__')

    def __init__(self,
        name: Optional[str] = None,
        registry: Optional[TBRegistry] = None,
    ):
        TBMain.count += 1
        self.name = name or f'TB-{TBMain.count}'
        self.registry = registry if registry else TBMain.registry
        self.runtimes = {}

    def __str__(self):
        return f"TBMain instance {self.name}"

    def context(self,
        system_prompt: Optional[str] = None,
    ):
        return TBContext(system_prompt)

    def model(self,
        model: str,
        **kwargs,
    ):
        model_parts = model.split('/')
        if len(model_parts) > 1:
            runtime_class = model_parts.pop(0)
            model = '/'.join(model_parts)
        else:
            runtime_class = self.registry.get_runtime_by_model(model)
        if runtime_class is None:
            raise Exception(f"Can't find runtime for model '{model}'")
        runtime = self.runtime(runtime_class)
        if runtime is None:
            raise Exception(f"Can't find runtime for runtime class '{runtime_class}'")
        return runtime.model(model, **kwargs)

    def chat(self,
        model: str,
        **kwargs,
    ):
        return self.model(model).chat(**kwargs)

    def runtime(self,
        runtime_class: str,
        **kwargs,
    ):
        if runtime_class in self.runtimes:
            return self.runtimes[runtime_class]
        try:
            from importlib import import_module
            from_list = [f"TBRuntime{runtime_class.title()}"]
            mod = import_module(f".runtime.{runtime_class}", package=__package__)
            self.runtimes[runtime_class] = getattr(mod, from_list[0])(**kwargs)
        except ImportError:
            mod = import_module(f"tackleberry.runtime.{runtime_class}")
            self.runtimes[runtime_class] = getattr(mod, f"TBRuntime{runtime_class.title()}")(**kwargs)
        if isinstance(self.runtimes[runtime_class], TBRuntime):
            return self.runtimes[runtime_class]
        else:
            raise Exception(f"Can't find runtime '{runtime_class}'")

TB = TBMain()

__all__ = ['TB']
