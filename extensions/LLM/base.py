from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseLLM(ABC):

    @abstractmethod
    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """
        it must return structured JSON output.
        """
        pass