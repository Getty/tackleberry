import unittest
import warnings
import os
from tackleberry import TB
from tackleberry.engine import TBEngine
from tackleberry.model import TBModel
from tackleberry.context import TBContext, TBMessage

class TestTB(unittest.TestCase):

    def test_000_unknown(self):
        """Test not existing Model and Engine"""
        with self.assertRaises(ModuleNotFoundError):
            engine = TB.engine('xxxxx')
        with self.assertRaises(KeyError):            
            model = TB.model('xxxxx')

    def test_001_openai(self):
        """Test OpenAI"""
        if os.environ.get("OPENAI_API_KEY"):
            engine = TB.engine('openai')
            self.assertIsInstance(engine, TBEngine)
            self.assertEqual(type(engine).__name__, "TBEngineOpenai")
            engine_model = engine.model('gpt-4o')
            self.assertIsInstance(engine_model, TBModel)
            self.assertEqual(type(engine_model).__name__, "TBModel")
            engine_slash_model = TB.model('openai/gpt-4o')
            self.assertIsInstance(engine_slash_model, TBModel)
            self.assertEqual(type(engine_slash_model).__name__, "TBModel")
            model = TB.model('gpt-4o')
            self.assertIsInstance(model, TBModel)
            self.assertEqual(type(model).__name__, "TBModel")
            self.assertIsInstance(model.engine, TBEngine)
            self.assertEqual(type(model.engine).__name__, "TBEngineOpenai")
            models = engine.get_models()
            self.assertTrue(len(models) > 20)
        else:
            warnings.warn("Can't test OpenAI engine without OPENAI_API_KEY", UserWarning)
    
    def test_002_anthropic(self):
        """Test Anthropic"""
        if os.environ.get("ANTHROPIC_API_KEY"):
            engine = TB.engine('anthropic')
            self.assertIsInstance(engine, TBEngine)
            self.assertEqual(type(engine).__name__, "TBEngineAnthropic")
            engine_model = engine.model('claude-2.1')
            self.assertIsInstance(engine_model, TBModel)
            self.assertEqual(type(engine_model).__name__, "TBModel")
            engine_slash_model = TB.model('anthropic/claude-2.1')
            self.assertIsInstance(engine_slash_model, TBModel)
            self.assertEqual(type(engine_slash_model).__name__, "TBModel")
            model = TB.model('claude-2.1')
            self.assertIsInstance(model, TBModel)
            self.assertEqual(type(model).__name__, "TBModel")
            self.assertIsInstance(model.engine, TBEngine)
            self.assertEqual(type(model.engine).__name__, "TBEngineAnthropic")
            models = engine.get_models()
            self.assertTrue(len(models) > 3)
        else:
            warnings.warn("Can't test Anthropic engine without ANTHROPIC_API_KEY", UserWarning)
    
    def test_003_groq(self):
        """Test Groq"""
        if os.environ.get("GROQ_API_KEY"):
            engine = TB.engine('groq')
            self.assertIsInstance(engine, TBEngine)
            self.assertEqual(type(engine).__name__, "TBEngineGroq")
            engine_model = engine.model('llama3-8b-8192')
            self.assertIsInstance(engine_model, TBModel)
            self.assertEqual(type(engine_model).__name__, "TBModel")
            engine_slash_model = TB.model('groq/llama3-8b-8192')
            self.assertIsInstance(engine_slash_model, TBModel)
            self.assertEqual(type(engine_slash_model).__name__, "TBModel")
            model = TB.model('llama3-8b-8192')
            self.assertIsInstance(model, TBModel)
            self.assertEqual(type(model).__name__, "TBModel")
            self.assertIsInstance(model.engine, TBEngine)
            self.assertEqual(type(model.engine).__name__, "TBEngineGroq")
            models = engine.get_models()
            self.assertTrue(len(models) > 10)
        else:
            warnings.warn("Can't test Groq engine without GROQ_API_KEY", UserWarning)

    def test_004_ollama(self):
        """Test Ollama"""
        if os.environ.get("OLLAMA_HOST") or os.environ.get("OLLAMA_PROXY_URL"):
            engine = TB.engine('ollama')
            self.assertIsInstance(engine, TBEngine)
            self.assertEqual(type(engine).__name__, "TBEngineOllama")
            models = engine.get_models()
            self.assertTrue(len(models) > 0)
        else:
            warnings.warn("Can't test Ollama engine without explicit setting OLLAMA_HOST or OLLAMA_PROXY_URL", UserWarning)

    def test_010_registry(self):
        """Test registry"""
        self.assertEqual(TB.count, 1)

    def test_020_context(self):
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