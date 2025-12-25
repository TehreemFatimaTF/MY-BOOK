"""
Query endpoints (POST /query)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from src.models.user_query import UserQuery, UserQueryCreate
from src.models.generated_response import GeneratedResponse
from src.services.rag_service import rag_service
from src.services.book_content_service import book_content_service
from src.middleware.auth import api_key_auth
from src.utils.logging import logger, log_error
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/query", response_model=GeneratedResponse)
async def query_book(user_query: UserQueryCreate, auth: bool = Depends(api_key_auth)):
    """
    Submit a query against a book's content
    """
    start_time = datetime.utcnow()

    try:
        # Validate query parameters
        if not user_query.book_id or len(user_query.book_id.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book ID is required"
            )

        if not user_query.query_text or len(user_query.query_text.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query text is required"
            )

        # Validate query text length
        if len(user_query.query_text) > 2000:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Query text is too long (max 2000 characters)"
            )

        # Validate selected text if provided
        if user_query.selected_text and len(user_query.selected_text) > 5000:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Selected text is too long (max 5000 characters)"
            )

        # Validate that the book exists
        book = await book_content_service.get_book(user_query.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {user_query.book_id} not found"
            )

        # Check if the book is ready for querying
        if book.status != "ready":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Book with ID {user_query.book_id} is not ready for queries (status: {book.status})"
            )

        # Create a UserQuery instance with a new ID
        query_instance = UserQuery(
            id=str(uuid.uuid4()),
            book_id=user_query.book_id,
            query_text=user_query.query_text,
            selected_text=user_query.selected_text,
            session_id=user_query.session_id,
            created_at=datetime.utcnow()
        )

        # Process the query through the RAG service
        response = await rag_service.process_query_with_validation(query_instance)

        # Calculate response time
        end_time = datetime.utcnow()
        response_time = (end_time - start_time).total_seconds()

        # Log the successful query with performance metrics
        logger.info(f"Query processed successfully for book {user_query.book_id} in {response_time:.2f}s")

        return response

    except HTTPException as e:
        # Log the HTTP exception
        logger.warning(f"HTTP error in query processing: {e.detail}")
        raise
    except ValueError as e:
        # Handle validation errors
        logger.warning(f"Validation error in query processing: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        # Handle other errors
        error_details = {
            "query_id": str(uuid.uuid4()) if 'query_instance' in locals() else "unknown",
            "book_id": user_query.book_id if 'user_query' in locals() else "unknown",
            "error_type": type(e).__name__,
            "error_message": str(e)
        }
        log_error(e, error_details)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while processing the query"
        )

# Streaming endpoint for query (T051 - will be implemented later)
# @router.post("/query/stream")
# async def query_book_streaming(user_query: UserQueryCreate, auth: bool = Depends(api_key_auth)):
#     """
#     Submit a query against a book's content with streaming response
#     """
#     # Implementation for streaming response would go here
#     pass

# Additional endpoint to validate query parameters
@router.post("/query/validate")
async def validate_query(user_query: UserQueryCreate, auth: bool = Depends(api_key_auth)):
    """
    Validate a query without processing it
    """
    try:
        # Check if the book exists
        book = await book_content_service.get_book(user_query.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {user_query.book_id} not found"
            )

        # Check if the book is ready for querying
        if book.status != "ready":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Book with ID {user_query.book_id} is not ready for queries (status: {book.status})"
            )

        # Basic validation of query text
        if not user_query.query_text or len(user_query.query_text.strip()) < 3:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Query text must be at least 3 characters long"
            )

        # If selected_text is provided, validate its length
        if user_query.selected_text and len(user_query.selected_text) > 5000:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Selected text is too long (max 5000 characters)"
            )

        # If selected_text is provided, validate that it's part of the book content
        if user_query.selected_text:
            book_content = await book_content_service.get_book_content(user_query.book_id)
            if not book_content:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Could not retrieve book content for validation"
                )

            # Simple check: verify that the selected text is part of the book content
            if user_query.selected_text not in book_content:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Selected text is not part of the book content"
                )

        return {
            "valid": True,
            "message": "Query is valid and ready for processing"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while validating the query: {str(e)}"
        )

# Streaming endpoint for query (T051)
@router.post("/query/stream")
async def query_book_streaming(user_query: UserQueryCreate, auth: bool = Depends(api_key_auth)):
    """
    Submit a query against a book's content with streaming response
    """
    try:
        # Validate that the book exists
        book = await book_content_service.get_book(user_query.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {user_query.book_id} not found"
            )

        # Check if the book is ready for querying
        if book.status != "ready":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Book with ID {user_query.book_id} is not ready for queries (status: {book.status})"
            )

        # Create a UserQuery instance with a new ID
        query_instance = UserQuery(
            id=str(uuid.uuid4()),
            book_id=user_query.book_id,
            query_text=user_query.query_text,
            selected_text=user_query.selected_text,
            session_id=user_query.session_id,
            created_at=datetime.utcnow()
        )

        # For now, return the same response as the regular query endpoint
        # In a real implementation, this would return an SSE (Server-Sent Events) stream
        response = await rag_service.process_query_with_validation(query_instance)

        # Log the successful query
        logger.info(f"Streaming query processed successfully for book {user_query.book_id}")

        return response

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
        logger.error(f"Error processing streaming query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the streaming query: {str(e)}"
        )