from typing import Any, Dict, Optional, Union

import copy

class TBMessage:
    """Base class for message"""
    def __init__(self, content: str, role: str):
        self.role = role
        self.content = content

class TBMessageSystem(TBMessage):
    """A system message"""
    def __init__(self, system_prompt: str):
        super().__init__(system_prompt, role="system")

class TBSystemPromptError(Exception):
    """Error to throw if system prompt is not possible in the way as used."""
    def __init__(self, message):
        super().__init__(message)

class TBMessageAssistant(TBMessage):
    """An AI assistant message"""
    def __init__(self, assistant_context: str):
        super().__init__(assistant_context, role="assistant")

class TBMessageUser(TBMessage):
    """User message"""
    def __init__(self, user_message: str, role: Optional[str] = None):
        super().__init__(user_message, role if role is not None else "user")

class TBContext:
    """Combined messages as context"""
    def __init__(self, system_prompt: Optional[str] = None, user_query: Optional[str] = None):
        self.messages = []
        self.query = user_query
        if not system_prompt is None:
            self.messages.append(TBMessageSystem(system_prompt))

    def add(self, message: TBMessage):
        self.messages.append(message)
        return self

    def add_system(self, system_prompt: str):
        self.messages.append(TBMessageSystem(system_prompt))
        return self

    def has_system(self):
        return any(isinstance(message, TBMessageSystem) for message in self.messages)

    def add_assistant(self, assistant_message: str):
        self.messages.append(TBMessageAssistant(assistant_message))
        return self

    def add_user(self, user_message: str):
        self.messages.append(TBMessageUser(user_message))
        return self

    def add_query(self, user_query: str):
        self.query = user_query
        return self

    def copy(self):
        return copy.deepcopy(self)

    def copy_with(self, message: Union[TBMessage, 'TBContext']):
        clone = self.copy()
        if isinstance(message, TBMessage):
            clone.add(message)
        elif isinstance(message, TBContext):
            for cmessage in message.messages:
                clone.add(cmessage)
        return clone

    def copy_with_system(self, system_prompt: str):
        return self.copy_with(TBMessageSystem(system_prompt))

    def copy_with_assistant(self, assistant_context: str):
        return self.copy_with(TBMessageAssistant(assistant_context))

    def copy_with_user(self, user_message: str):
        return self.copy_with(TBMessageUser(user_message))

    def copy_with_query(self, user_query: str):
        return self.copy().add_query(user_query)

    def get_messages(self):
        messages = self.messages
        if not self.query is None:
            messages.append(TBMessageUser(self.query))
        return messages

    def to_messages(self):
        message_list = []
        for message in self.get_messages():
            message_list.append({
                "content": message.content,
                "role": message.role,
            })
        return message_list