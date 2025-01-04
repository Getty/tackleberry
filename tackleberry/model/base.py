from typing import Any, Dict, Optional

from ..engine import TBEngine

class TBModel:

    def __init__(self, engine: TBEngine, name: str):
        self.engine = engine
        self.name = name
