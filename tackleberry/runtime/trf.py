from .base import TBRuntime

class TBRuntimeTrf(TBRuntime):

    def __init__(self,
        hf_token: str = None,
        **kwargs,
    ):
        self.hf_token = hf_token

    def __str__(self):
        return f"TB Runtime HuggingFace transformers {hex(id(self))}"
