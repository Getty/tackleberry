import os
import importlib

# Special case: Explicitly import TBRuntime from base.py
from .base import TBRuntime

# Automatically detect all Python files in the current directory
current_dir = os.path.dirname(__file__)
module_files = [
    f for f in os.listdir(current_dir)
    if f.endswith(".py") and f not in ("__init__.py", "base.py")
]

# Create __all__ with the module names and the special case
__all__ = ["TBRuntime"] + [os.path.splitext(f)[0] for f in module_files]

# Dynamically import the modules and add them to the global namespace
for module_name in __all__[1:]:  # Skip "TBRuntime" as it's already imported
    module = importlib.import_module(f".{module_name}", package=__name__)
    globals()[module_name] = module