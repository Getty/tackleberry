from .base import TBEngine

class TBEngineTrf(TBEngine):

    def __init__(self,
        hf_token: str = None,
        **kwargs,
    ):
        self.hf_token = hf_token

    def __str__(self):
        return f"TB Engine HuggingFace transformers {hex(id(self))}"
