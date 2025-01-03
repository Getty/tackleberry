from typing import Any, Union, Dict, List, Optional
import os

from . import TBEngine

class TBEngineHf(TBEngine):

    def __init__(self,
        hf_token: str = None,
        **kwargs,
    ):
        self.hf_token = hf_token

    def __str__(self):
        return f"TB Engine HuggingFace {hex(id(self))}"
