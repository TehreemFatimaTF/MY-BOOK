"""
Additional API routes for React frontend integration
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from pydantic import BaseModel
from src.services.rag_service import rag_service
from src.services.book_content_service import book_content_service
from src.middleware.auth import api_key_auth
from src.utils.logging import logger
import uuid
from datetime import datetime

router = APIRouter()

# Request models for the React frontend
class AskRequest(BaseModel):
    message: str
    book_id: str
    session_id: Optional[str] = None

class AskSelectionRequest(BaseModel):
    message: str
    selected_text: str
    book_id: str
    session_id: Optional[str] = None

# Response model
class ChatResponse(BaseModel):
    response: str
    query_id: str
    timestamp: datetime

@router.post("/api/ask", response_model=ChatResponse)
async def ask_endpoint(request: AskRequest, auth: bool = Depends(api_key_auth)):
    """
    Endpoint for normal chat (matches React frontend expectation)
    """
    try:
        # Validate that the book exists
        book = await book_content_service.get_book(request.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {request.book_id} not found"
            )
        
        # Check if the book is ready for querying
        if book.status != "ready":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Book with ID {request.book_id} is not ready for queries (status: {book.status})"
            )
        
        # Create a UserQuery instance
        from src.models.user_query import UserQuery
        user_query = UserQuery(
            id=str(uuid.uuid4()),
            book_id=request.book_id,
            query_text=request.message,
            selected_text=None,  # Not using selected text for normal chat
            session_id=request.session_id,
            created_at=datetime.utcnow()
        )
        
        # Process the query through the RAG service
        response = await rag_service.process_query_with_validation(user_query)
        
        # Log the successful query
        logger.info(f"Normal chat query processed successfully for book {request.book_id}")
        
        return ChatResponse(
            response=response.response_text,
            query_id=response.query_id,
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        # Handle other errors
        logger.error(f"Error processing normal chat query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the query: {str(e)}"
        )

@router.post("/api/ask-selection", response_model=ChatResponse)
async def ask_selection_endpoint(request: AskSelectionRequest, auth: bool = Depends(api_key_auth)):
    """
    Endpoint for text selection-based chat (matches React frontend expectation)
    """
    try:
        # Validate that the book exists
        book = await book_content_service.get_book(request.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {request.book_id} not found"
            )
        
        # Check if the book is ready for querying
        if book.status != "ready":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Book with ID {request.book_id} is not ready for queries (status: {book.status})"
            )
        
        # Validate that the selected text is part of the book content
        book_content = await book_content_service.get_book_content(request.book_id)
        if not book_content:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not retrieve book content for validation"
            )
        
        # Check if the selected text is part of the book content
        if request.selected_text not in book_content:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Selected text is not part of the book content"
            )
        
        # Create a UserQuery instance with selected text
        from src.models.user_query import UserQuery
        user_query = UserQuery(
            id=str(uuid.uuid4()),
            book_id=request.book_id,
            query_text=request.message,
            selected_text=request.selected_text,
            session_id=request.session_id,
            created_at=datetime.utcnow()
        )
        
        # Process the query through the RAG service
        response = await rag_service.process_query_with_validation(user_query)
        
        # Log the successful query
        logger.info(f"Text selection query processed successfully for book {request.book_id}")
        
        return ChatResponse(
            response=response.response_text,
            query_id=response.query_id,
            timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        # Handle other errors
        logger.error(f"Error processing text selection query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the selection query: {str(e)}"
        )

# Additional utility endpoints
@router.get("/api/health")
async def frontend_health_check():
    """
    Health check endpoint for the frontend
    """
    return {
        "status": "healthy",
        "service": "book-rag-chatbot-backend",
        "timestamp": datetime.utcnow().isoformat()
    }