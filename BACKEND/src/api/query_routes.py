"""
Query endpoints (POST /query) - Security Disabled for Development
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from src.models.user_query import UserQuery, UserQueryCreate
from src.models.generated_response import GeneratedResponse
from src.services.rag_service import rag_service
from src.services.book_content_service import book_content_service
# Security hatane ke liye auth import aur api_key_auth ko nikal diya gaya hai
from src.utils.logging import logger, log_error
import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/query", response_model=GeneratedResponse)
async def query_book(user_query: UserQueryCreate):
    """
    Submit a query against a book's content (Open Access)
    """
    print(f"DEBUG: Received query: {user_query}")
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

        # Validate that the book exists
        book = await book_content_service.get_book(user_query.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {user_query.book_id} not found"
            )

        # Check if the book is ready
        if book.status != "ready":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Book with ID {user_query.book_id} is not ready (status: {book.status})"
            )

        # Create query instance
        query_instance = UserQuery(
            id=str(uuid.uuid4()),
            book_id=user_query.book_id,
            query_text=user_query.query_text,
            selected_text=user_query.selected_text,
            session_id=user_query.session_id,
            created_at=datetime.utcnow()
        )

        response = await rag_service.process_query_with_validation(query_instance)

        end_time = datetime.utcnow()
        response_time = (end_time - start_time).total_seconds()
        logger.info(f"Query processed successfully in {response_time:.2f}s")

        return response

    except HTTPException:
        raise
    except Exception as e:
        log_error(e, {"book_id": user_query.book_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error occurred"
        )

@router.post("/query/validate")
async def validate_query(user_query: UserQueryCreate):
    """
    Validate a query (Open Access)
    """
    book = await book_content_service.get_book(user_query.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"valid": True, "message": "Ready for processing"}

@router.post("/query/stream")
async def query_book_streaming(user_query: UserQueryCreate):
    """
    Streaming query (Open Access)
    """
    query_instance = UserQuery(
        id=str(uuid.uuid4()),
        book_id=user_query.book_id,
        query_text=user_query.query_text,
        selected_text=user_query.selected_text,
        session_id=user_query.session_id,
        created_at=datetime.utcnow()
    )
    return await rag_service.process_query_with_validation(query_instance)
