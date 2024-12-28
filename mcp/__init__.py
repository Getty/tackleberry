from importlib.metadata import version
from mcp.__main__ import MCP

__all__ = ['MCP']

try:
    __version__ = version("mcp")
except ImportError:
    __version__ = "0.0.0"
