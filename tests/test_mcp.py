import unittest
import warnings
import os
from mcp import MCP
from mcp.engine import MCPEngine
from mcp.model import MCPModel
from mcp.context import MCPContext, MCPMessage

class TestMCP(unittest.TestCase):

    def test_000_unknown(self):
        """Test not existing Model and Engine"""
        with self.assertRaises(ModuleNotFoundError):
            engine = MCP.engine('xxxxx')
        with self.assertRaises(KeyError):            
            model = MCP.model('xxxxx')

    def test_001_openai(self):
        """Test OpenAI"""
        if os.environ.get("OPENAI_API_KEY"):
            engine = MCP.engine('openai')
            self.assertIsInstance(engine, MCPEngine)
            self.assertEqual(type(engine).__name__, "MCPEngineOpenai")
            engine_model = engine.model('gpt-4o')
            self.assertIsInstance(engine_model, MCPModel)
            self.assertEqual(type(engine_model).__name__, "MCPModel")
            engine_slash_model = MCP.model('openai/gpt-4o')
            self.assertIsInstance(engine_slash_model, MCPModel)
            self.assertEqual(type(engine_slash_model).__name__, "MCPModel")
            model = MCP.model('gpt-4o')
            self.assertIsInstance(model, MCPModel)
            self.assertEqual(type(model).__name__, "MCPModel")
            self.assertIsInstance(model.engine, MCPEngine)
            self.assertEqual(type(model.engine).__name__, "MCPEngineOpenai")
            models = engine.get_models()
            self.assertTrue(len(models) > 20)
        else:
            warnings.warn("Can't test OpenAI engine without OPENAI_API_KEY", UserWarning)
    
    def test_002_anthropic(self):
        """Test Anthropic"""
        if os.environ.get("ANTHROPIC_API_KEY"):
            engine = MCP.engine('anthropic')
            self.assertIsInstance(engine, MCPEngine)
            self.assertEqual(type(engine).__name__, "MCPEngineAnthropic")
            engine_model = engine.model('claude-2.1')
            self.assertIsInstance(engine_model, MCPModel)
            self.assertEqual(type(engine_model).__name__, "MCPModel")
            engine_slash_model = MCP.model('anthropic/claude-2.1')
            self.assertIsInstance(engine_slash_model, MCPModel)
            self.assertEqual(type(engine_slash_model).__name__, "MCPModel")
            model = MCP.model('claude-2.1')
            self.assertIsInstance(model, MCPModel)
            self.assertEqual(type(model).__name__, "MCPModel")
            self.assertIsInstance(model.engine, MCPEngine)
            self.assertEqual(type(model.engine).__name__, "MCPEngineAnthropic")
            models = engine.get_models()
            self.assertTrue(len(models) > 3)
        else:
            warnings.warn("Can't test Anthropic engine without ANTHROPIC_API_KEY", UserWarning)
    
    def test_003_groq(self):
        """Test Groq"""
        if os.environ.get("GROQ_API_KEY"):
            engine = MCP.engine('groq')
            self.assertIsInstance(engine, MCPEngine)
            self.assertEqual(type(engine).__name__, "MCPEngineGroq")
            engine_model = engine.model('llama3-8b-8192')
            self.assertIsInstance(engine_model, MCPModel)
            self.assertEqual(type(engine_model).__name__, "MCPModel")
            engine_slash_model = MCP.model('groq/llama3-8b-8192')
            self.assertIsInstance(engine_slash_model, MCPModel)
            self.assertEqual(type(engine_slash_model).__name__, "MCPModel")
            model = MCP.model('llama3-8b-8192')
            self.assertIsInstance(model, MCPModel)
            self.assertEqual(type(model).__name__, "MCPModel")
            self.assertIsInstance(model.engine, MCPEngine)
            self.assertEqual(type(model.engine).__name__, "MCPEngineGroq")
            models = engine.get_models()
            self.assertTrue(len(models) > 10)
        else:
            warnings.warn("Can't test Groq engine without GROQ_API_KEY", UserWarning)

    def test_004_ollama(self):
        """Test Ollama"""
        if os.environ.get("OLLAMA_HOST") or os.environ.get("OLLAMA_PROXY_URL"):
            engine = MCP.engine('ollama')
            self.assertIsInstance(engine, MCPEngine)
            self.assertEqual(type(engine).__name__, "MCPEngineOllama")
            models = engine.get_models()
            self.assertTrue(len(models) > 0)
        else:
            warnings.warn("Can't test Ollama engine without explicit setting OLLAMA_HOST or OLLAMA_PROXY_URL", UserWarning)

    def test_010_registry(self):
        """Test registry"""
        self.assertEqual(MCP.count, 1)

    def test_020_context(self):
        """Test context"""
        nosys_context = MCP.context()
        self.assertIsInstance(nosys_context, MCPContext)
        self.assertTrue(len(nosys_context.messages) == 0)
        nosys_context.add_system("you are an assistant")
        self.assertTrue(len(nosys_context.messages) == 1)
        self.assertEqual(nosys_context.to_messages(), [{
            'content': 'you are an assistant',
            'role': 'system',
        }])
        sys_context = MCP.context("you are an assistant that hates his work")
        self.assertIsInstance(sys_context, MCPContext)
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