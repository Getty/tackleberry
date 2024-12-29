from importlib.metadata import version
from .__main__ import TB

__all__ = ['TB']

try:
    __version__ = version("tackleberry")
except ImportError:
    __version__ = "0.0.0"
