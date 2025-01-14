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

class TestTBAnthropic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise unittest.SkipTest("Skipping all tests because ANTHROPIC_API_KEY environment variable is not set.")

    def test_010_standard_query(self):
        """Test Standard Query"""
        # SYNOPSIS TEST
        chat = TB.chat('claude-3-haiku-20240307')
        self.assertIsInstance(chat, TBChat)
        reply = chat.query("Say test")
        self.assertTrue(len(reply) > 0, "Reply shouldn't be empty")

    def test_020_structured_output(self):
        """Test Structured Output"""
        chat = TB.chat('claude-3-haiku-20240307')
        user_info = chat.query("Extract the name and the age: 'John is 20 years old'", UserInfo)
        self.assertIsInstance(user_info, UserInfo)
        self.assertEqual(user_info.name, "John")
        self.assertEqual(user_info.age, 20)
    
if __name__ == "__main__":
    unittest.main()