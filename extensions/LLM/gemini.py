import google.generativeai as genai
import json
from typing import Dict, Any
from engine.config import GEMINI_API_KEY


class GeminiClient:
    """Simple wrapper around Gemini for getting JSON responses only."""

    def __init__(self, model = "gemini-1.5-flash"):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model)

    def generate_json(self, prompt) -> Dict[str, Any]:
        """
        Ask Gemini and return structured JSON.
        """

        full_prompt = f"""
        Respond ONLY in valid JSON, Nothing else.
        No explanation.
        No markdown.

        {prompt}
        """

        response = self.model.generate_content(full_prompt)
        text = response.text.strip()

        try:
            return json.loads(text)
        except Exception:
            raise ValueError(f"LLM returned non JSON output:\n{text}")
