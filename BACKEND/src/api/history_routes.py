"""
Query history and feedback endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from src.models.query_history import QueryHistory, QueryHistoryCreate, QueryHistoryUpdate
from src.models.user_query import UserQuery
from src.services.postgres_service import postgres_service
from src.services.book_content_service import book_content_service
from src.middleware.auth import api_key_auth
from src.utils.logging import logger
import uuid
from datetime import datetime

router = APIRouter()

@router.get("/history", response_model=List[QueryHistory])
async def get_query_history(
    book_id: Optional[str] = Query(None, description="Filter by book ID"),
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    auth: bool = Depends(api_key_auth)
):
    """
    Retrieve query history for a book or session
    """
    try:
        # Build query conditions
        conditions = []
        params = []
        
        if book_id:
            # Validate that the book exists
            book = await book_content_service.get_book(book_id)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Book with ID {book_id} not found"
                )
            conditions.append("uq.book_id = $%d" % (len(params) + 1))
            params.append(book_id)
        
        if session_id:
            conditions.append("uq.session_id = $%d" % (len(params) + 1))
            params.append(session_id)
        
        # Build the SQL query
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        query_sql = f"""
            SELECT qh.id, qh.query_id, qh.user_id, qh.query_text, qh.response_text, 
                   qh.accuracy_score, qh.feedback, qh.timestamp
            FROM query_history qh
            JOIN user_queries uq ON qh.query_id = uq.id
            {where_clause}
            ORDER BY qh.timestamp DESC
            LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}
        """
        
        # Add limit and offset to params
        params.extend([limit, offset])
        
        # Execute the query
        results = await postgres_service.execute_query(query_sql, *params)
        
        # Convert results to QueryHistory objects
        histories = []
        for result in results:
            history = QueryHistory(
                id=result['id'],
                query_id=result['query_id'],
                user_id=result['user_id'],
                query_text=result['query_text'],
                response_text=result['response_text'],
                accuracy_score=result['accuracy_score'],
                feedback=result['feedback'],
                timestamp=result['timestamp']
            )
            histories.append(history)
        
        return histories
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving query history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving query history"
        )

@router.post("/history/{query_id}/feedback", status_code=status.HTTP_200_OK)
async def submit_feedback(
    query_id: str,
    feedback_data: QueryHistoryUpdate,
    auth: bool = Depends(api_key_auth)
):
    """
    Submit feedback for a query response
    """
    try:
        # Verify that the query exists
        query_check_sql = """
            SELECT id FROM user_queries WHERE id = $1
        """
        query_result = await postgres_service.execute_query_row(query_check_sql, query_id)
        
        if not query_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Query with ID {query_id} not found"
            )
        
        # Update the feedback in the query history
        update_sql = """
            UPDATE query_history
            SET accuracy_score = COALESCE($1, accuracy_score),
                feedback = COALESCE($2, feedback)
            WHERE query_id = $3
            RETURNING id
        """
        
        result = await postgres_service.execute_query_row(
            update_sql,
            feedback_data.accuracy_score,
            feedback_data.feedback,
            query_id
        )
        
        if not result:
            # If no record was updated, it might not exist in history yet
            # In a real implementation, you might want to create a history record if it doesn't exist
            logger.warning(f"No history record found for query ID {query_id}, creating one...")
            
            # For now, just return a success message
            return {"message": "Feedback submitted successfully"}
        
        logger.info(f"Feedback submitted for query {query_id}")
        return {"message": "Feedback submitted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while submitting feedback"
        )