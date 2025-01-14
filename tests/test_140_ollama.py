import unittest
import warnings
import os
from unittest.mock import patch
import requests
from tackleberry import TB
from tackleberry.chat import TBChat
from tackleberry.context import TBContext
from pydantic import BaseModel

import sys

class UserInfo(BaseModel):
    name: str
    age: int

class TestTBOllama(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.environ.get("OLLAMA_HOST") or os.environ.get("OLLAMA_PROXY_URL"):
            raise unittest.SkipTest("Skipping all tests because OLLAMA_HOST and OLLAMA_PROXY_URL environment variables are not set.")
        cls.ollama_model = os.environ.get("TACKLEBERRY_OLLAMA_TEST_MODEL") or 'gemma2:2b'
        cls.ollama_chat = TB.chat('ollama/'+cls.ollama_model, num_ctx=512, temperature=0)

    def test_000_ollama_chat(self):
        self.assertIsInstance(self.ollama_chat, TBChat)

    def test_010_standard_query(self):
        """Test Standard Query"""
        # SYNOPSIS TEST
        ollama_reply = TestTBOllama.ollama_chat.query("Say test")
        self.assertTrue(len(ollama_reply) > 0, "Reply shouldn't be empty")

    def test_020_structured_output(self):
        """Test Structured Output"""
        # SYNOPSIS TEST
        ollama_user_info = TestTBOllama.ollama_chat.query("Extract the name and the age: 'John is 20 years old'", UserInfo)
        self.assertIsInstance(ollama_user_info, UserInfo)
        self.assertEqual(ollama_user_info.name, "John")
        self.assertEqual(ollama_user_info.age, 20)
    
if __name__ == "__main__":
    unittest.main()