from openai import OpenAI
from src.config.settings import settings
from src.utils.logging import logger, ExternalServiceError
from typing import List, Optional, Dict, Any

class OpenRouterService:
    def __init__(self):
        if not settings.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is not set")
            
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )
        self.model = "google/gemini-2.0-flash-001" # Default to Gemini on OpenRouter
        
    def generate_response(
        self, 
        prompt: str, 
        context: Optional[str] = None,
        max_tokens: Optional[int] = 1000
    ) -> str:
        try:
            messages = []
            if context:
                messages.append({"role": "system", "content": f"Use the following context to answer:\n{context}"})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.3
            )
            
            if not response.choices or not response.choices[0].message.content:
                raise ExternalServiceError("OpenRouter", "Empty response from OpenRouter")
                
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating response with OpenRouter: {e}")
            raise ExternalServiceError("OpenRouter", str(e))

# Global instance
openrouter_service = OpenRouterService()
