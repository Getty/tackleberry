import unittest
import warnings
import os
from unittest.mock import patch
import requests
from tackleberry import TB
from tackleberry.runtime import TBRuntime
from tackleberry.model import TBModel
from tackleberry.chat import TBChat
from tackleberry.context import TBContext, TBMessage

class TestTB(unittest.TestCase):

    def test_000_unknown(self):
        """Test not existing Model and Runtime"""
        with self.assertRaises(ModuleNotFoundError):
            runtime = TB.runtime('xxxxx')
        with self.assertRaises(KeyError):
            model = TB.model('xxxxx')
        with self.assertRaises(KeyError):
            chat = TB.chat('xxxxx')

    def test_010_openai(self):
        """Test OpenAI"""
        if os.environ.get("OPENAI_API_KEY"):
            runtime = TB.runtime('openai')
            self.assertIsInstance(runtime, TBRuntime)
            self.assertEqual(type(runtime).__name__, "TBRuntimeOpenai")
            runtime_model = runtime.model('gpt-4o')
            self.assertIsInstance(runtime_model, TBModel)
            self.assertEqual(type(runtime_model).__name__, "TBModel")
            runtime_slash_model = TB.model('openai/gpt-4o')
            self.assertIsInstance(runtime_slash_model, TBModel)
            self.assertEqual(type(runtime_slash_model).__name__, "TBModel")
            model = TB.model('gpt-4o')
            self.assertIsInstance(model, TBModel)
            self.assertEqual(type(model).__name__, "TBModel")
            self.assertIsInstance(model.runtime, TBRuntime)
            self.assertEqual(type(model.runtime).__name__, "TBRuntimeOpenai")
            chat = TB.chat('gpt-4o')
            self.assertIsInstance(chat, TBChat)
            self.assertEqual(type(chat).__name__, "TBChat")
            models = runtime.get_models()
            self.assertTrue(len(models) > 20)
        else:
            warnings.warn("Can't test OpenAI runtime without OPENAI_API_KEY", UserWarning)
    
    def test_020_anthropic(self):
        """Test Anthropic"""
        if os.environ.get("ANTHROPIC_API_KEY"):
            runtime = TB.runtime('anthropic')
            self.assertIsInstance(runtime, TBRuntime)
            self.assertEqual(type(runtime).__name__, "TBRuntimeAnthropic")
            runtime_model = runtime.model('claude-2.1')
            self.assertIsInstance(runtime_model, TBModel)
            self.assertEqual(type(runtime_model).__name__, "TBModel")
            runtime_slash_model = TB.model('anthropic/claude-2.1')
            self.assertIsInstance(runtime_slash_model, TBModel)
            self.assertEqual(type(runtime_slash_model).__name__, "TBModel")
            model = TB.model('claude-2.1')
            self.assertIsInstance(model, TBModel)
            self.assertEqual(type(model).__name__, "TBModel")
            self.assertIsInstance(model.runtime, TBRuntime)
            self.assertEqual(type(model.runtime).__name__, "TBRuntimeAnthropic")
            chat = TB.chat('claude-2.1')
            self.assertIsInstance(chat, TBChat)
            self.assertEqual(type(chat).__name__, "TBChat")
            models = runtime.get_models()
            self.assertTrue(len(models) > 3)
        else:
            warnings.warn("Can't test Anthropic runtime without ANTHROPIC_API_KEY", UserWarning)
    
    def test_030_groq(self):
        """Test Groq"""
        if os.environ.get("GROQ_API_KEY"):
            runtime = TB.runtime('groq')
            self.assertIsInstance(runtime, TBRuntime)
            self.assertEqual(type(runtime).__name__, "TBRuntimeGroq")
            runtime_model = runtime.model('llama3-8b-8192')
            self.assertIsInstance(runtime_model, TBModel)
            self.assertEqual(type(runtime_model).__name__, "TBModel")
            runtime_slash_model = TB.model('groq/llama3-8b-8192')
            self.assertIsInstance(runtime_slash_model, TBModel)
            self.assertEqual(type(runtime_slash_model).__name__, "TBModel")
            model = TB.model('llama3-8b-8192')
            self.assertIsInstance(model, TBModel)
            self.assertEqual(type(model).__name__, "TBModel")
            self.assertIsInstance(model.runtime, TBRuntime)
            self.assertEqual(type(model.runtime).__name__, "TBRuntimeGroq")
            chat = TB.chat('llama3-8b-8192')
            self.assertIsInstance(chat, TBChat)
            self.assertEqual(type(chat).__name__, "TBChat")
            models = runtime.get_models()
            self.assertTrue(len(models) > 10)
        else:
            warnings.warn("Can't test Groq runtime without GROQ_API_KEY", UserWarning)

    def test_040_ollama(self):
        """Test Ollama"""
        if os.environ.get("OLLAMA_HOST") or os.environ.get("OLLAMA_PROXY_URL"):
            from tackleberry.runtime.ollama import TBRuntimeOllama
            runtime = TB.runtime('ollama')
            self.assertIsInstance(runtime, TBRuntime)
            self.assertEqual(type(runtime).__name__, "TBRuntimeOllama")
            models = runtime.get_models()
            self.assertTrue(len(models) > 0)
        else:
            warnings.warn("Can't test Ollama runtime without explicit setting OLLAMA_HOST or OLLAMA_PROXY_URL", UserWarning)

    @patch('httpx.Client.send')
    def test_041_ollama_userpass(self, mock_send):
        """Test Ollama user pass to basic auth conversion"""
        if os.environ.get("OLLAMA_HOST") or os.environ.get("OLLAMA_PROXY_URL"):
            from tackleberry.runtime.ollama import TBRuntimeOllama
            mock_response = unittest.mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"models": []}

            mock_send.return_value = mock_response

            runtime = TBRuntimeOllama(
                url = 'https://user:pass@domain.com:5000',
            )
            self.assertEqual(type(runtime).__name__, "TBRuntimeOllama")

            models = runtime.get_models()

            # Assert: Verify the request details
            mock_send.assert_called_once()
            request, kwargs = mock_send.call_args

            self.assertEqual(request[0].method, 'GET')
            self.assertEqual(request[0].url, 'https://domain.com:5000/api/tags')
            self.assertEqual(request[0].headers['authorization'], 'Basic dXNlcjpwYXNz')
        else:
            warnings.warn("Can't test Ollama runtime without explicit setting OLLAMA_HOST or OLLAMA_PROXY_URL", UserWarning)

    def test_100_registry(self):
        """Test registry"""
        self.assertEqual(TB.count, 1)

    def test_200_context(self):
        """Test context"""
        nosys_context = TB.context()
        self.assertIsInstance(nosys_context, TBContext)
        self.assertTrue(len(nosys_context.messages) == 0)
        nosys_context.add_system("you are an assistant")
        self.assertTrue(len(nosys_context.messages) == 1)
        self.assertEqual(nosys_context.to_messages(), [{
            'content': 'you are an assistant',
            'role': 'system',
        }])
        sys_context = TB.context("you are an assistant that hates his work")
        self.assertIsInstance(sys_context, TBContext)
        self.assertTrue(len(sys_context.messages) == 1)
        sys_context.add_assistant("roger rabbit is a fictional animated anthropomorphic rabbit")
        self.assertTrue(len(sys_context.messages) == 2)
        sys_context.add_user("who is roger rabbit?")
        self.assertTrue(len(sys_context.messages) == 3)
        self.assertEqual(sys_context.to_messages(), [{
            'content': 'you are an assistant that hates his work',
            'role': 'system',
        }, {
            'content': 'roger rabbit is a fictional animated anthropomorphic rabbit',
            'role': 'assistant',
        }, {
            'content': 'who is roger rabbit?',
            'role': 'user',
        }])

if __name__ == "__main__":
    unittest.main()