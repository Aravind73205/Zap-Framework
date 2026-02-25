import json
from typing import Dict, Any

from google import genai
from google.genai.errors import ClientError

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
  
            text = response.text.strip()
            return json.loads(text)       
    
        except ClientError as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
    
        except Exception as e:
            raise RuntimeError(f"[Gemini unexpected error]: {str(e)}")
