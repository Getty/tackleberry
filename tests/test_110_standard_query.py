import unittest
import warnings
import os
from unittest.mock import patch
import requests
from tackleberry import TB

import sys

class TestTB(unittest.TestCase):

    def test_010_openai(self):
        """Test OpenAI"""
        if os.environ.get("OPENAI_API_KEY"):
            chat = TB.chat('openai/gpt-4o-mini')
            test_resp = chat.query("Say test")
        else:
            warnings.warn("Can't test OpenAI runtime without OPENAI_API_KEY", UserWarning)
    
    def test_020_anthropic(self):
        """Test Anthropic"""
        if os.environ.get("ANTHROPIC_API_KEY"):
            chat = TB.chat('anthropic/claude-3-5-haiku-20241022')
            test_resp = chat.query("Say test")
        else:
            warnings.warn("Can't test Anthropic runtime without ANTHROPIC_API_KEY", UserWarning)
    
    def test_030_groq(self):
        """Test Groq"""
        if os.environ.get("GROQ_API_KEY"):
            chat = TB.chat('groq/llama3-8b-8192')
            test_resp = chat.query("Say test")
        else:
            warnings.warn("Can't test Groq runtime without GROQ_API_KEY", UserWarning)

    def test_040_ollama(self):
        """Test Ollama"""
        ollama_model = os.environ.get("TACKLEBERRY_OLLAMA_TEST_MODEL") or 'gemma2:2b'
        if (os.environ.get("OLLAMA_HOST") or os.environ.get("OLLAMA_PROXY_URL")) and ollama_model:
            chat = TB.chat('ollama/'+ollama_model)
            test_resp = chat.query("Say test")
        else:
            warnings.warn("Can't test Ollama runtime without explicit setting OLLAMA_HOST or OLLAMA_PROXY_URL", UserWarning)

if __name__ == "__main__":
    unittest.main()