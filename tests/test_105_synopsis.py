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

class TestTB(unittest.TestCase):

    def test_010_openai(self):
        """Test OpenAI"""
        if os.environ.get("OPENAI_API_KEY"):
            openai_chat = TB.chat('gpt-4o-mini')
            self.assertIsInstance(openai_chat, TBChat)
            openai_reply = openai_chat.query("Say test")
            self.assertTrue(len(openai_reply) > 0, "Reply shouldn't be empty")
        else:
            warnings.warn("Can't test OpenAI runtime without OPENAI_API_KEY", UserWarning)
    
    def test_020_anthropic(self):
        """Test Anthropic"""
        if os.environ.get("ANTHROPIC_API_KEY"):
            claude_chat = TB.chat('claude-3-5-sonnet-20241022')
            self.assertIsInstance(claude_chat, TBChat)
            claude_reply = claude_chat.query("Say test")
            self.assertTrue(len(claude_reply) > 0, "Reply shouldn't be empty")
        else:
            warnings.warn("Can't test Anthropic runtime without ANTHROPIC_API_KEY", UserWarning)
    
    def test_030_groq(self):
        """Test Groq"""
        if os.environ.get("GROQ_API_KEY"):
            groq_chat = TB.chat('gemma2-9b-it')
            self.assertIsInstance(groq_chat, TBChat)
            groq_reply = groq_chat.query("Say test")
            self.assertTrue(len(groq_reply) > 0, "Reply shouldn't be empty")
            groq_user_info = groq_chat.query("Extract the name and the age: 'John is 20 years old'", UserInfo)
            self.assertIsInstance(groq_user_info, UserInfo)
            self.assertEqual(groq_user_info.name, "John")
            self.assertEqual(groq_user_info.age, 20)
        else:
            warnings.warn("Can't test Groq runtime without GROQ_API_KEY", UserWarning)

    def test_040_ollama(self):
        """Test Ollama"""
        ollama_model = os.environ.get("TACKLEBERRY_OLLAMA_TEST_MODEL") or 'gemma2:2b'
        if os.environ.get("OLLAMA_HOST") or os.environ.get("OLLAMA_PROXY_URL"):
            ollama_chat = TB.chat('ollama/'+ollama_model)
            self.assertIsInstance(ollama_chat, TBChat)
            ollama_reply = ollama_chat.query("Say test")
            self.assertTrue(len(ollama_reply) > 0, "Reply shouldn't be empty")
            ollama_user_info = ollama_chat.query("Extract the name and the age: 'John is 20 years old'", UserInfo)
            self.assertIsInstance(ollama_user_info, UserInfo)
            self.assertEqual(ollama_user_info.name, "John")
            self.assertEqual(ollama_user_info.age, 20)
        else:
            warnings.warn("Can't test Ollama runtime without explicit setting OLLAMA_HOST or OLLAMA_PROXY_URL", UserWarning)

if __name__ == "__main__":
    unittest.main()