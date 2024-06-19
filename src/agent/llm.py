"""
Interfaces the AI Agent to the LLM Provider, model availability depends on
implemented prompts, to use a new model the relative prompts should be written.

LLM providers are:
- [x] Ollama
- [ ] HuggingFace
"""
from ollama import Client
from dataclasses import dataclass

AVAILABLE_MODELS = ['phi3', 'gemma:2b', 'gemma:7b']


@dataclass
class LLM:
    """Ollama model interface"""
    model: str
    client_url: str = 'http://localhost:11434'

    def __post_init__(self):
        if self.model not in AVAILABLE_MODELS:
            raise ValueError(f'Model {self.model} is not available')
        self.client = Client(self.client_url)

    def query(self, messages: list, stream=True):
        """Generator that returns response chunks from Phi3-mini-k4 model"""
        return self.client.chat(
            model=self.model,
            messages=messages,
            stream=stream,
        )


if __name__ == "__main__":
    llm = LLM('gemma:2b')
    out = llm.query([
        {'role': 'user', 'content': 'How do I build a search engine?'}
    ])

    for chunk in out:
        print(chunk['message']['content'], end='')
