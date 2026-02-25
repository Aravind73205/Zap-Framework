import json
from typing import Dict, Any

from google import genai
from engine.config import GEMINI_API_KEY, GEMINI_MODEL
from extensions.llm.base import BaseLLM


class GeminiClient(BaseLLM):

    def __init__(self):   
        if not GEMINI_API_KEY:
            raise ValueError("Gemini Api Key not found in environment variables")
        
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = GEMINI_MODEL

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        
        # Gemini sometimes ignores "ONLY JSON", so we force it hard
        full_prompt = f"""
        Respond ONLY in valid JSON, Nothing else.
        No explanation.
        No markdown.

        {prompt}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
            )
        except Exception as api_error:
            raise RuntimeError(f"[Gemini API Error] {str(api_error)}")
        

        text = response.text.strip()       

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(f"[Gemini json Parse Error] Model returned invalid JSON:\n{text}")
