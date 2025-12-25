"""
Unit test for Cohere service integration
"""
import pytest
from unittest.mock import Mock, patch
from src.services.cohere_service import CohereService

def test_cohere_service_generate_response():
    """
    Unit test for Cohere service generate_response method
    """
    # Mock the Cohere client
    with patch('cohere.Client') as mock_cohere_client:
        # Set up the mock
        mock_client_instance = Mock()
        mock_client_instance.chat.return_value = Mock(text="Generated response from Cohere")
        mock_cohere_client.return_value = mock_client_instance
        
        # Create CohereService instance
        cohere_service = CohereService()
        
        # Test data
        prompt = "What is this book about?"
        context = "This is the context from the book..."
        
        # Execute the method
        response = cohere_service.generate_response(prompt, context)
        
        # Verify the response
        assert response == "Generated response from Cohere"
        
        # Verify that the Cohere client was called with correct parameters
        mock_client_instance.chat.assert_called_once()
        call_args = mock_client_instance.chat.call_args
        assert "message" in call_args.kwargs
        assert prompt in call_args.kwargs["message"]
        
        print("Cohere service generate_response unit test passed")

def test_cohere_service_generate_response_with_history():
    """
    Unit test for Cohere service with conversation history
    """
    # Mock the Cohere client
    with patch('cohere.Client') as mock_cohere_client:
        # Set up the mock
        mock_client_instance = Mock()
        mock_client_instance.chat.return_value = Mock(text="Response considering conversation history")
        mock_cohere_client.return_value = mock_client_instance
        
        # Create CohereService instance
        cohere_service = CohereService()
        
        # Test data
        prompt = "What was the previous topic?"
        context = "Previous conversation context..."
        conversation_history = [
            {"user": "What is this book about?", "bot": "This book is about AI and machine learning."},
            {"user": "Can you explain neural networks?", "bot": "Neural networks are computing systems..."}
        ]
        
        # Execute the method
        response = cohere_service.generate_response(prompt, context, conversation_history)
        
        # Verify the response
        assert response == "Response considering conversation history"
        
        # Verify that the Cohere client was called
        mock_client_instance.chat.assert_called_once()
        
        print("Cohere service generate_response with history unit test passed")

def test_cohere_service_handle_error():
    """
    Unit test for Cohere service error handling
    """
    # Mock the Cohere client to raise an exception
    with patch('cohere.Client') as mock_cohere_client:
        # Set up the mock to raise an exception
        mock_client_instance = Mock()
        mock_client_instance.chat.side_effect = Exception("API Error")
        mock_cohere_client.return_value = mock_client_instance
        
        # Create CohereService instance
        cohere_service = CohereService()
        
        # Test data
        prompt = "What is this book about?"
        context = "This is the context from the book..."
        
        # Execute the method and expect an exception
        with pytest.raises(Exception) as exc_info:
            cohere_service.generate_response(prompt, context)
        
        # Verify the exception
        assert "API Error" in str(exc_info.value)
        
        print("Cohere service error handling unit test passed")

if __name__ == "__main__":
    test_cohere_service_generate_response()
    test_cohere_service_generate_response_with_history()
    test_cohere_service_handle_error()