from typing import Any, Dict, Optional

class TBEngine:

    def __init__(self):
        pass

    def model(self, model: str):
        from ..model import TBModel
        return TBModel(self, model)
