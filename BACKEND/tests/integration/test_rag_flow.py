"""
Integration test for RAG flow with book content
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.rag_service import RAGService
from src.models.book_content import BookContent
from src.models.user_query import UserQuery
from src.utils.embedding_utils import CohereEmbeddingService

def test_rag_flow_integration():
    """
    Integration test for the complete RAG flow:
    1. Take user query
    2. Generate embedding for the query
    3. Search for relevant context in Qdrant
    4. Generate response using Cohere
    """
    
    # Mock the services that will be used in the RAG flow
    with patch('src.services.cohere_service.CohereService') as mock_cohere_service, \
         patch('src.services.qdrant_service.QdrantService') as mock_qdrant_service, \
         patch('src.services.postgres_service.PostgresService') as mock_postgres_service:
        
        # Set up mock return values
        mock_cohere_service.generate_response.return_value = "Test response from Cohere"
        mock_qdrant_service.search.return_value = [
            {"id": "chunk-1", "content": "Relevant content from the book", "score": 0.9}
        ]
        mock_postgres_service.get_book_content.return_value = "Full book content here..."
        
        # Create an instance of RAGService with mocked dependencies
        rag_service = RAGService(
            cohere_service=mock_cohere_service,
            qdrant_service=mock_qdrant_service,
            postgres_service=mock_postgres_service
        )
        
        # Prepare test data
        book_content = BookContent(
            id="test-book-id",
            title="Test Book",
            author="Test Author",
            content="This is the content of the test book. It contains information about various topics.",
            content_hash="test-hash"
        )
        
        user_query = UserQuery(
            id="test-query-id",
            book_id="test-book-id",
            query_text="What is this book about?",
            created_at="2025-12-24T00:00:00Z"
        )
        
        # Execute the RAG flow
        result = rag_service.process_query(user_query)
        
        # Verify the flow
        assert result is not None
        assert "Test response from Cohere" in result.response_text
        
        # Verify that the correct methods were called
        mock_cohere_service.generate_response.assert_called_once()
        mock_qdrant_service.search.assert_called_once()
        
        print("RAG flow integration test passed")

def test_rag_flow_with_selected_text():
    """
    Integration test for RAG flow with user-selected text
    """
    
    # Mock the services that will be used in the RAG flow
    with patch('src.services.cohere_service.CohereService') as mock_cohere_service, \
         patch('src.services.qdrant_service.QdrantService') as mock_qdrant_service, \
         patch('src.services.postgres_service.PostgresService') as mock_postgres_service:
        
        # Set up mock return values
        mock_cohere_service.generate_response.return_value = "Test response based on selected text"
        mock_qdrant_service.search.return_value = [
            {"id": "chunk-1", "content": "Selected text content", "score": 0.95}
        ]
        mock_postgres_service.get_book_content.return_value = "Full book content here..."
        
        # Create an instance of RAGService with mocked dependencies
        rag_service = RAGService(
            cohere_service=mock_cohere_service,
            qdrant_service=mock_qdrant_service,
            postgres_service=mock_postgres_service
        )
        
        # Prepare test data with selected text
        user_query = UserQuery(
            id="test-query-id",
            book_id="test-book-id",
            query_text="Explain this concept",
            selected_text="This is the specific text the user selected",
            created_at="2025-12-24T00:00:00Z"
        )
        
        # Execute the RAG flow with selected text
        result = rag_service.process_query(user_query)
        
        # Verify the flow
        assert result is not None
        assert "Test response based on selected text" in result.response_text
        
        # For selected text queries, we might not call Qdrant search but rather process the selected text directly
        # This depends on the implementation details
        mock_cohere_service.generate_response.assert_called_once()
        
        print("RAG flow with selected text integration test passed")

if __name__ == "__main__":
    test_rag_flow_integration()
    test_rag_flow_with_selected_text()