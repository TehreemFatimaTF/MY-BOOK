"""
PostgresService implementation for metadata storage
"""
from typing import List, Optional, Dict, Any
from src.db.postgres_client import postgres_client
from src.models.book_content import BookContent
from src.models.user_query import UserQuery
from src.models.retrieved_context import RetrievedContext
from src.models.generated_response import GeneratedResponse
from src.models.query_history import QueryHistory
from src.utils.logging import logger
import uuid
from datetime import datetime

class PostgresService:
    def __init__(self):
        # Initialize the postgres_client if not already done
        pass
    
    async def initialize(self):
        """
        Initialize the service and ensure connection pool is ready
        """
        if not postgres_client.pool:
            await postgres_client.initialize_pool()
    
    async def store_query(self, user_query: UserQuery) -> str:
        """
        Store a user query in the database
        """
        try:
            query = """
                INSERT INTO user_queries (id, book_id, query_text, selected_text, session_id, created_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
            """
            
            result = await postgres_client.execute_query_row(
                query,
                user_query.id,
                user_query.book_id,
                user_query.query_text,
                user_query.selected_text,
                user_query.session_id,
                user_query.created_at
            )
            
            logger.info(f"Stored query with ID: {result['id']}")
            return result['id']
            
        except Exception as e:
            logger.error(f"Error storing query in Postgres: {e}")
            raise
    
    async def store_retrieved_context(self, contexts: List[RetrievedContext]):
        """
        Store retrieved contexts in the database
        """
        try:
            for context in contexts:
                query = """
                    INSERT INTO retrieved_contexts (id, query_id, content_chunk, chunk_id, relevance_score, retrieved_at)
                    VALUES ($1, $2, $3, $4, $5, $6)
                """
                
                context_id = str(uuid.uuid4()) if not context.id or context.id.startswith('test-') else context.id
                await postgres_client.execute_command(
                    query,
                    context_id,
                    context.query_id,
                    context.content_chunk,
                    context.chunk_id,
                    context.relevance_score,
                    context.retrieved_at
                )
            
            logger.info(f"Stored {len(contexts)} retrieved contexts in Postgres")
            
        except Exception as e:
            logger.error(f"Error storing retrieved contexts in Postgres: {e}")
            raise
    
    async def store_generated_response(self, response: GeneratedResponse):
        """
        Store generated response in the database
        """
        try:
            query = """
                INSERT INTO generated_responses (id, query_id, response_text, confidence_score, source_chunks, generated_at)
                VALUES ($1, $2, $3, $4, $5, $6)
            """
            
            response_id = str(uuid.uuid4()) if not response.id or response.id.startswith('test-') else response.id
            await postgres_client.execute_command(
                query,
                response_id,
                response.query_id,
                response.response_text,
                response.confidence_score,
                response.source_chunks,
                response.generated_at
            )
            
            logger.info(f"Stored generated response with ID: {response_id}")
            
        except Exception as e:
            logger.error(f"Error storing generated response in Postgres: {e}")
            raise
    
    async def store_query_history(self, query_history: QueryHistory):
        """
        Store query history in the database
        """
        try:
            query = """
                INSERT INTO query_history (id, query_id, user_id, query_text, response_text, accuracy_score, feedback, timestamp)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """
            
            history_id = str(uuid.uuid4()) if not query_history.id or query_history.id.startswith('test-') else query_history.id
            await postgres_client.execute_command(
                query,
                history_id,
                query_history.query_id,
                query_history.user_id,
                query_history.query_text,
                query_history.response_text,
                query_history.accuracy_score,
                query_history.feedback,
                query_history.timestamp
            )
            
            logger.info(f"Stored query history with ID: {history_id}")
            
        except Exception as e:
            logger.error(f"Error storing query history in Postgres: {e}")
            raise
    
    async def get_book_content(self, book_id: str) -> Optional[str]:
        """
        Retrieve the full content of a book by ID
        """
        try:
            query = """
                SELECT content
                FROM book_content
                WHERE id = $1
            """
            result = await postgres_client.execute_query_row(query, book_id)
            
            if result:
                return result['content']
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving book content from Postgres: {e}")
            raise
    
    async def get_relevant_queries(self, book_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get relevant past queries for a book to provide context
        """
        try:
            query = """
                SELECT uq.query_text, gr.response_text
                FROM user_queries uq
                JOIN generated_responses gr ON uq.id = gr.query_id
                WHERE uq.book_id = $1
                ORDER BY uq.created_at DESC
                LIMIT $2
            """
            results = await postgres_client.execute_query(query, book_id, limit)
            
            relevant_queries = []
            for result in results:
                relevant_queries.append({
                    "query": result['query_text'],
                    "response": result['response_text']
                })
            
            return relevant_queries
            
        except Exception as e:
            logger.error(f"Error retrieving relevant queries from Postgres: {e}")
            raise
    
    async def get_user_feedback_stats(self, book_id: str) -> Dict[str, Any]:
        """
        Get feedback statistics for a book
        """
        try:
            # Get average accuracy score
            avg_score_query = """
                SELECT AVG(accuracy_score) as avg_accuracy
                FROM query_history qh
                JOIN user_queries uq ON qh.query_id = uq.id
                WHERE uq.book_id = $1 AND qh.accuracy_score IS NOT NULL
            """
            avg_result = await postgres_client.execute_query_row(avg_score_query, book_id)
            
            # Get feedback count
            feedback_count_query = """
                SELECT COUNT(*) as feedback_count
                FROM query_history qh
                JOIN user_queries uq ON qh.query_id = uq.id
                WHERE uq.book_id = $1 AND qh.feedback IS NOT NULL
            """
            count_result = await postgres_client.execute_query_row(feedback_count_query, book_id)
            
            return {
                "average_accuracy": float(avg_result['avg_accuracy']) if avg_result['avg_accuracy'] else 0.0,
                "feedback_count": int(count_result['feedback_count']) if count_result['feedback_count'] else 0
            }
            
        except Exception as e:
            logger.error(f"Error retrieving feedback stats from Postgres: {e}")
            raise

# Global instance
postgres_service = PostgresService()
