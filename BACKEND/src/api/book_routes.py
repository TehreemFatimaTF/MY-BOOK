"""
Book management endpoints (POST /books, GET /books, GET /books/{book_id})
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.models.book_content import BookContent, BookContentCreate
from src.pipeline.book_ingestion import book_ingestion_pipeline
from src.services.book_content_service import book_content_service
from src.middleware.auth import api_key_auth
import uuid

router = APIRouter()

@router.post("/books", response_model=BookContent, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookContentCreate, auth: bool = Depends(api_key_auth)):
    """
    Upload a new book for RAG querying
    """
    try:
        # Create the book via the ingestion pipeline
        book_id = await book_ingestion_pipeline.ingest_book(
            title=book_data.title,
            author=book_data.author,
            content=book_data.content,
            isbn=book_data.isbn
        )
        
        # Retrieve the created book
        created_book = await book_content_service.get_book(book_id)
        
        if not created_book:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Book was created but could not be retrieved"
            )
        
        return created_book
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the book: {str(e)}"
        )

@router.get("/books/{book_id}", response_model=BookContent)
async def get_book(book_id: str, auth: bool = Depends(api_key_auth)):
    """
    Retrieve information about a specific book
    """
    try:
        book = await book_content_service.get_book(book_id)
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        
        return book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the book: {str(e)}"
        )

@router.get("/books", response_model=List[BookContent])
async def list_books(auth: bool = Depends(api_key_auth)):
    """
    List all available books
    """
    try:
        books = await book_content_service.list_books()
        return books
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while listing books: {str(e)}"
        )

# Additional endpoint to check ingestion status
@router.get("/books/{book_id}/status")
async def get_book_status(book_id: str, auth: bool = Depends(api_key_auth)):
    """
    Get the processing status of a book
    """
    try:
        book = await book_content_service.get_book(book_id)
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        
        return {
            "book_id": book.id,
            "status": book.status,
            "title": book.title,
            "author": book.author
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while getting book status: {str(e)}"
        )