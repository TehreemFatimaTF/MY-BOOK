"""
CohereService implementation for text generation
"""
import cohere
from typing import List, Optional, Dict, Any
from src.config.settings import settings
from src.utils.logging import logger, ExternalServiceError
from src.models.generated_response import GeneratedResponse
import hashlib

class CohereService:
    def __init__(self):
        if not settings.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set")

        self.client = cohere.Client(settings.cohere_api_key)
        self.model = settings.cohere_model
        # Simple in-memory cache for embeddings
        self.embedding_cache = {}
        self.cache_size_limit = 1000  # Limit cache size to prevent memory issues
    
    def generate_response(
        self, 
        prompt: str, 
        context: Optional[str] = None, 
        conversation_history: Optional[List[Dict[str, str]]] = None,
        max_tokens: Optional[int] = 500
    ) -> str:
        """
        Generate a response using Cohere's language model
        """
        try:
            # Prepare the message with context if provided
            if context:
                message = f"Context: {context}\n\nQuestion: {prompt}\n\nPlease provide an accurate answer based solely on the provided context."
            else:
                message = f"Question: {prompt}\n\nPlease provide an accurate answer."
            
            # Prepare the chat history if provided
            chat_history = []
            if conversation_history:
                for entry in conversation_history:
                    # Add user message
                    chat_history.append({"role": "USER", "message": entry.get("user", "")})
                    # Add bot message
                    chat_history.append({"role": "CHATBOT", "message": entry.get("bot", "")})
            
            # Call Cohere's chat API
            response = self.client.chat(
                message=message,
                model=self.model,
                chat_history=chat_history if chat_history else None,
                max_tokens=max_tokens,
                temperature=0.3  # Lower temperature for more consistent, factual responses
            )
            
            if not response or not response.text:
                raise ExternalServiceError("Cohere", "No response text returned from Cohere API")
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response with Cohere: {e}")
            raise ExternalServiceError("Cohere", str(e))
    
    def generate_response_with_citations(
        self, 
        prompt: str, 
        context: Optional[str] = None,
        sources: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response with potential citations to sources
        """
        try:
            # Prepare the message with context and source information
            message_parts = []
            if context:
                message_parts.append(f"Context: {context}")
            
            if sources:
                message_parts.append(f"Sources: {', '.join(sources)}")
            
            message_parts.append(f"Question: {prompt}")
            message_parts.append("Please provide an accurate answer based solely on the provided context and cite sources where appropriate.")
            
            message = "\n\n".join(message_parts)
            
            # Call Cohere's chat API
            response = self.client.chat(
                message=message,
                model=self.model,
                temperature=0.3
            )
            
            if not response or not response.text:
                raise ExternalServiceError("Cohere", "No response text returned from Cohere API")
            
            result = {
                "text": response.text,
                "citations": []  # Cohere doesn't directly provide citations, but we can structure for future use
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating response with citations using Cohere: {e}")
            raise ExternalServiceError("Cohere", str(e))
    
    def check_coherence(self, response: str, context: str) -> float:
        """
        Check how coherent the response is with the provided context
        This is a simplified implementation - in practice, you might use more sophisticated methods
        """
        try:
            # Create a prompt to evaluate coherence
            evaluation_prompt = f"""
            Context: {context}
            
            Response: {response}
            
            On a scale of 0 to 1, how well does the response align with and accurately reflect the content in the provided context? 
            0 means completely unrelated or contradictory, 1 means perfectly aligned and accurate.
            Please respond with just the number.
            """
            
            coherence_score_text = self.client.chat(
                message=evaluation_prompt,
                model=self.model,
                temperature=0.1
            ).text
            
            # Extract the score from the response (should be a number between 0 and 1)
            try:
                # Try to extract a float from the response
                import re
                numbers = re.findall(r"[\d.]+", coherence_score_text)
                if numbers:
                    score = float(numbers[0])
                    return min(1.0, max(0.0, score))  # Clamp between 0 and 1
            except:
                pass
            
            # If we can't parse the response, default to a conservative score
            return 0.5
            
        except Exception as e:
            logger.error(f"Error checking coherence with Cohere: {e}")
            return 0.5  # Return neutral score on error

    def embed_text_with_caching(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for texts with caching for frequently used texts
        """
        results = []

        for text in texts:
            # Create a cache key based on the text content
            text_hash = hashlib.sha256(text.encode()).hexdigest()

            # Check if embedding is already in cache
            if text_hash in self.embedding_cache:
                results.append(self.embedding_cache[text_hash])
                continue

            # Generate embedding using the utility function
            from src.utils.embedding_utils import cohere_embedding_service
            embedding = cohere_embedding_service.embed_single_text(text)

            # Add to cache if we're under the size limit
            if len(self.embedding_cache) < self.cache_size_limit:
                self.embedding_cache[text_hash] = embedding

            results.append(embedding)

        return results

# Global instance
cohere_service = CohereService()
