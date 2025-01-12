from importlib.metadata import version
from .main import TB

__all__ = ['TB']

try:
    __version__ = version("tackleberry")
except ImportError:
    __version__ = "0.0.1.dev1"
