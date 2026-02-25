import time
from typing import Dict, Any

from extensions.llm.base import BaseLLM


class RetryLLM(BaseLLM):
    """
    wrapper that adds retry behavior
    to any LLM implementation following BaseLLM.
    """

    def __init__(self, llm: BaseLLM, max_attempts: int = 2, delay_seconds: int = 1):
        self.llm = llm
        self.max_attempts = max_attempts
        self.delay_seconds = delay_seconds

    def generate_json(self, prompt: str) -> Dict[str, Any]:

        attempt = 0

        while attempt < self.max_attempts:
            try:
                return self.llm.generate_json(prompt)

            except Exception as e:
                if attempt == self.max_attempts - 1:
                    raise  # re raise after final attempt

                attempt += 1
                time.sleep(self.delay_seconds)