import json
from typing import Dict, Any

from google import genai
from engine.config import GEMINI_API_KEY
from extensions.llm.base import BaseLLM


class GeminiClient(BaseLLM):

    def __init__(self, model = "gemini-3-flash-preview"):   
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = model

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        
        # Gemini sometimes ignores "ONLY JSON", so we force it hard
        full_prompt = f"""
        Respond ONLY in valid JSON, Nothing else.
        No explanation.
        No markdown.

        {prompt}
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
        )

        text = response.text.strip()

        try:
            return json.loads(text)
        except Exception:
            raise ValueError(f"LLM returned non JSON output:\n{text}")
