"""
Interfaces the AI Agent to the LLM Provider, model availability depends on
implemented prompts, to use a new model the relative prompts should be written.

LLM providers are:
- [x] Ollama
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from ollama import Client

AVAILABLE_MODELS = {
    'llama3': {
        'options': {
            'temperature': 0.5,
            'num_ctx': 8192
        }
    },
    'gemma:7b': {
        'options': {
            'temperature': 0.5,
            'num_ctx': 8192
        }
    },
    'mistral': {
        'options': {
            'temperature': 0.5,
            'num_ctx': 8192
        }
    },
}


@dataclass
class Provider(ABC):
    """Represents a LLM Provider"""
    model: str
    client_url: str = 'http://localhost:11434'
    api_key: str | None = None

    @abstractmethod
    def query(self, messages: list, stream=True):
        """Implement to makes query to the LLM provider"""


class Ollama(Provider):
    """Ollama Interface"""
    def __post_init__(self):
        if self.model not in AVAILABLE_MODELS.keys():
            raise ValueError(f'Model {self.model} is not available')
        self.client = Client(self.client_url)

    def query(self, messages: list, stream=True):
        """Generator that returns response chunks."""
        return self.client.chat(
            model=self.model,
            messages=messages,
            stream=stream,
            options=AVAILABLE_MODELS[self.model]['options']
        )


@dataclass
class LLM:
    """Ollama model interface"""
    model: str
    client_url: str = 'http://localhost:11434'
    provider: Provider = Ollama

    def query(self, messages: list, stream=True):
        """Generator that returns response chunks."""
        return self.provider.query(messages, stream=stream)
