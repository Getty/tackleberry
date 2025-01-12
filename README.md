[![Tackleberry](https://raw.githubusercontent.com/Getty/tackleberry/main/tackleberry.jpg)](https://github.com/Getty/tackleberry)

# Tackleberry

API may change slightly, still work in progress.

## Synopsis

```python
from tackleberry import TB

openai_chat = TB.chat('gpt-4o-mini')
openai_reply = openai_chat.query("Say test")

claude_chat = TB.chat('claude-3-5-sonnet-20241022')
claude_reply = claude_chat.query("Say test")

# OLLAMA_PROXY_URL set for URL, can handle Basic Auth in URL
ollama_chat = TB.chat('ollama/gemma2:2b')
ollama_reply = ollama_chat.query("Say test")

from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str
    age: int

# Using Structured Output Feature of Ollama - no instructor
ollama_user_info = ollama_chat.query("Extract the name and the age: 'John is 20 years old'", UserInfo)

# Using instructor[anthropic]
claude_user_info = claude_chat.query("Extract the name and the age: 'John is 20 years old'", UserInfo)

```

# Install

## Using PIP

### Stable Version with PIP

Install from `PyPi`

```console
❯ pip install --upgrade tackleberry
```

