"""
RAGService implementation orchestrating the RAG flow
"""
from typing import List, Optional, Dict, Any
from src.services.cohere_service import CohereService
from src.services.qdrant_service import QdrantService
from src.services.postgres_service import PostgresService
from src.models.user_query import UserQuery
from src.models.retrieved_context import RetrievedContext
from src.models.generated_response import GeneratedResponse
from src.models.query_history import QueryHistory
from src.utils.logging import logger, log_query_execution
from src.utils.text_chunker import TextChunker
import uuid
from datetime import datetime

class RAGService:
    def __init__(self, cohere_service=None, qdrant_service=None, postgres_service=None):
        self.cohere_service = cohere_service or CohereService()
        self.qdrant_service = qdrant_service or QdrantService()
        self.postgres_service = postgres_service or PostgresService()
        self.text_chunker = TextChunker()
    
    async def process_query(self, user_query: UserQuery) -> GeneratedResponse:
        """
        Process a user query through the complete RAG pipeline
        """
        try:
            # Log the query execution
            query_id = user_query.id or str(uuid.uuid4())
            logger.info(f"Processing query: '{user_query.query_text[:50]}...' for book {user_query.book_id}")
            
            # Step 1: Store the user query in the database
            if not user_query.id:
                user_query.id = query_id
            await self.postgres_service.store_query(user_query)
            
            # Step 2: Retrieve relevant context based on query type
            retrieved_contexts = []
            
            if user_query.selected_text:
                # If user has selected specific text, search within that context
                retrieved_contexts = self.qdrant_service.search_with_selected_text(
                    selected_text=user_query.selected_text,
                    query_text=user_query.query_text,
                    book_id=user_query.book_id
                )

                # Validate that the selected text is part of the book content
                await self._validate_selected_text(user_query.book_id, user_query.selected_text)
            else:
                # Otherwise, search the entire book
                retrieved_contexts = self.qdrant_service.search(
                    query_text=user_query.query_text,
                    book_id=user_query.book_id
                )
            
            # Step 3: Create RetrievedContext objects and store them
            context_objects = []
            for i, ctx in enumerate(retrieved_contexts):
                context_obj = RetrievedContext(
                    id=f"{query_id}_ctx_{i}",
                    query_id=query_id,
                    content_chunk=ctx["content"],
                    chunk_id=ctx["id"],
                    relevance_score=ctx["relevance_score"],
                    retrieved_at=datetime.utcnow()
                )
                context_objects.append(context_obj)
            
            await self.postgres_service.store_retrieved_context(context_objects)
            
            # Step 4: Prepare context for generation
            if not retrieved_contexts:
                if user_query.selected_text:
                    # For selected text queries, use the selected text as context
                    context_text = f"Selected text: {user_query.selected_text}"
                else:
                    context_text = "No relevant content found in the book to answer this question."
            else:
                # Combine the top contexts
                context_parts = [ctx["content"] for ctx in retrieved_contexts]
                context_text = "\n\n".join(context_parts)
            
            # Step 5: Generate response using Cohere
            response_text = self.cohere_service.generate_response(
                prompt=user_query.query_text,
                context=context_text
            )
            
            # Step 6: Create and store the generated response
            generated_response = GeneratedResponse(
                id=str(uuid.uuid4()),
                query_id=query_id,
                response_text=response_text,
                confidence_score=None,  # Will be calculated in a real implementation
                source_chunks=[ctx["id"] for ctx in retrieved_contexts],
                generated_at=datetime.utcnow()
            )
            
            await self.postgres_service.store_generated_response(generated_response)
            
            # Step 7: Create and store query history
            query_history = QueryHistory(
                id=str(uuid.uuid4()),
                query_id=query_id,
                user_id=None,  # Would come from authentication in real implementation
                query_text=user_query.query_text,
                response_text=response_text,
                accuracy_score=None,  # Would be set later based on feedback
                feedback=None,
                timestamp=datetime.utcnow()
            )
            
            await self.postgres_service.store_query_history(query_history)
            
            # Log the execution
            log_query_execution(
                query_id=query_id,
                book_id=user_query.book_id,
                query_text=user_query.query_text,
                response_length=len(response_text)
            )
            
            logger.info(f"Query {query_id} processed successfully")
            return generated_response
            
        except Exception as e:
            logger.error(f"Error processing query in RAGService: {e}")
            raise
    
    async def process_query_with_validation(self, user_query: UserQuery) -> GeneratedResponse:
        """
        Process a user query with additional validation and quality checks
        """
        try:
            # Validate query
            if len(user_query.query_text.strip()) < 3:
                raise ValueError("Query must be at least 3 characters long")
            
            # Process the query normally
            response = await self.process_query(user_query)
            
            # Perform additional validation on the response
            # Check if response is grounded in provided context
            if not self._is_response_groundedin_context(response.response_text, user_query.query_text):
                logger.warning(f"Response may not be fully grounded in context for query {user_query.id}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query with validation in RAGService: {e}")
            raise
    
    def _is_response_groundedin_context(self, response: str, query: str) -> bool:
        """
        Basic check to see if the response is related to the query
        This is a simplified implementation - in practice, you'd use more sophisticated methods
        """
        # Convert to lowercase for comparison
        response_lower = response.lower()
        query_lower = query.lower()
        
        # Simple check: does the response contain key terms from the query?
        query_words = query_lower.split()
        if not query_words:
            return True  # If no query words, consider valid
        
        # Count how many query words appear in the response
        matches = sum(1 for word in query_words if word in response_lower)
        
        # If at least half the query words appear in the response, consider it grounded
        return matches >= len(query_words) // 2

    async def _validate_selected_text(self, book_id: str, selected_text: str) -> bool:
        """
        Validate that the selected text is part of the book content
        """
        # Get the book content
        book_content = await self.postgres_service.get_book_content(book_id)

        if not book_content:
            raise ValueError(f"Book content not found for book ID: {book_id}")

        # Check if the selected text is part of the book content
        if selected_text not in book_content:
            raise ValueError("Selected text is not part of the book content")

        return True

    async def process_batch_queries(self, queries: List[UserQuery]) -> List[GeneratedResponse]:
        """
        Process multiple queries in batch
        """
        responses = []
        for query in queries:
            try:
                response = await self.process_query(query)
                responses.append(response)
            except Exception as e:
                logger.error(f"Error processing batch query {query.id}: {e}")
                # Depending on requirements, you might want to continue processing other queries
                # or fail the entire batch
                raise

        return responses
    
    async def get_conversation_context(self, session_id: Optional[str] = None, book_id: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Get conversation context for maintaining context across queries
        """
        context = []
        
        if session_id:
            # In a real implementation, you would retrieve conversation history for the session
            # For now, we'll return an empty list
            pass
        
        if book_id:
            # Get relevant past queries for the book
            try:
                relevant_queries = await self.postgres_service.get_relevant_queries(book_id, limit=5)
                context.extend(relevant_queries)
            except Exception as e:
                logger.warning(f"Could not retrieve relevant queries for book {book_id}: {e}")
        
        return context

# Global instance
rag_service = RAGService()