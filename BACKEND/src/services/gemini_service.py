import google.generativeai as genai
from src.config.settings import settings
from src.utils.logging import logger, ExternalServiceError
from typing import List, Optional, Dict, Any

class GeminiService:
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest') # Using gemini-flash-latest
        
    def generate_response(
        self, 
        prompt: str, 
        context: Optional[str] = None,
        max_tokens: Optional[int] = 1000
    ) -> str:
        try:
            full_prompt = ""
            if context:
                full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}\n\nPlease answer based on the context."
            else:
                full_prompt = prompt
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.3
                )
            )
            
            if not response or not response.text:
                raise ExternalServiceError("Gemini", "Empty response from Gemini")
                
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response with Gemini: {e}")
            raise ExternalServiceError("Gemini", str(e))

# Global instance
gemini_service = GeminiService()
