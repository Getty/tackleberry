import unittest
import warnings
import os
from mcp import MCP
from mcp.engine import MCPEngine
from mcp.model import MCPModel

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
            engine_slash_model = engine.model('openai/gpt-4o')
            self.assertIsInstance(engine_slash_model, MCPModel)
            self.assertEqual(type(engine_slash_model).__name__, "MCPModel")
            model = MCP.model('gpt-4o')
            self.assertIsInstance(model, MCPModel)
            self.assertEqual(type(model).__name__, "MCPModel")
            self.assertIsInstance(model.engine, MCPEngine)
            self.assertEqual(type(model.engine).__name__, "MCPEngineOpenai")
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
            engine_slash_model = engine.model('anthropic/claude-2.1')
            self.assertIsInstance(engine_slash_model, MCPModel)
            self.assertEqual(type(engine_slash_model).__name__, "MCPModel")
            model = MCP.model('claude-2.1')
            self.assertIsInstance(model, MCPModel)
            self.assertEqual(type(model).__name__, "MCPModel")
            self.assertIsInstance(model.engine, MCPEngine)
            self.assertEqual(type(model.engine).__name__, "MCPEngineAnthropic")
        else:
            warnings.warn("Can't test Anthropic engine without ANTHROPIC_API_KEY", UserWarning)
    
    def test_003_groq(self):
        """Test Anthropic"""
        if os.environ.get("GROQ_API_KEY"):
            engine = MCP.engine('groq')
            self.assertIsInstance(engine, MCPEngine)
            self.assertEqual(type(engine).__name__, "MCPEngineGroq")
            engine_model = engine.model('llama3-8b-8192')
            self.assertIsInstance(engine_model, MCPModel)
            self.assertEqual(type(engine_model).__name__, "MCPModel")
            engine_slash_model = engine.model('groq/llama3-8b-8192')
            self.assertIsInstance(engine_slash_model, MCPModel)
            self.assertEqual(type(engine_slash_model).__name__, "MCPModel")
            model = MCP.model('llama3-8b-8192')
            self.assertIsInstance(model, MCPModel)
            self.assertEqual(type(model).__name__, "MCPModel")
            self.assertIsInstance(model.engine, MCPEngine)
            self.assertEqual(type(model.engine).__name__, "MCPEngineGroq")
        else:
            warnings.warn("Can't test Anthropic engine without GROQ_API_KEY", UserWarning)

    def test_010_registry(self):
        """Test registry"""
        self.assertEqual(MCP.count, 1)

if __name__ == "__main__":
    unittest.main()