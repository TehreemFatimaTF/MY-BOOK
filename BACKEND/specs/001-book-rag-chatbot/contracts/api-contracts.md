# API Contracts: Book RAG Chatbot

**Feature**: 001-book-rag-chatbot
**Date**: 2025-12-24

## Overview
This document defines the API contracts for the Book RAG Chatbot feature, specifying endpoints, request/response formats, and error handling.

## Base URL
`http://localhost:8000/api` (or configured base URL)

## Authentication
All API requests require a valid API key sent in the `Authorization` header:
```
Authorization: Bearer <your-api-key>
```

## Endpoints

### 1. Book Management

#### POST /books
Upload a new book for RAG querying.

**Request Body**:
```json
{
  "title": "string (required)",
  "author": "string (required)",
  "isbn": "string (optional)",
  "content": "string (required, book content)"
}
```

**Response (201 Created)**:
```json
{
  "id": "string (UUID)",
  "title": "string",
  "author": "string",
  "isbn": "string",
  "created_at": "datetime",
  "status": "processing|ready|failed"
}
```

**Error Responses**:
- 400: Invalid request body
- 401: Unauthorized
- 422: Validation error

#### GET /books/{book_id}
Retrieve information about a specific book.

**Response (200 OK)**:
```json
{
  "id": "string (UUID)",
  "title": "string",
  "author": "string",
  "isbn": "string",
  "content_hash": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "status": "processing|ready|failed"
}
```

**Error Responses**:
- 401: Unauthorized
- 404: Book not found

#### GET /books
List all available books.

**Response (200 OK)**:
```json
{
  "books": [
    {
      "id": "string (UUID)",
      "title": "string",
      "author": "string",
      "isbn": "string",
      "created_at": "datetime",
      "status": "processing|ready|failed"
    }
  ],
  "total": "integer"
}
```

**Error Responses**:
- 401: Unauthorized

### 2. Query Processing

#### POST /query
Submit a query against a book's content.

**Request Body**:
```json
{
  "book_id": "string (UUID, required)",
  "query_text": "string (required, the question to answer)",
  "selected_text": "string (optional, specific text selected by user)",
  "session_id": "string (optional, for tracking conversation context)"
}
```

**Response (200 OK)**:
```json
{
  "id": "string (UUID)",
  "query_text": "string",
  "response_text": "string",
  "retrieved_contexts": [
    {
      "chunk_id": "string",
      "content": "string",
      "relevance_score": "float"
    }
  ],
  "confidence_score": "float (optional)",
  "timestamp": "datetime"
}
```

**Error Responses**:
- 400: Invalid request body
- 401: Unauthorized
- 404: Book not found
- 422: Validation error
- 500: Processing error

#### POST /query/stream
Submit a query against a book's content with streaming response.

**Request Body**:
```json
{
  "book_id": "string (UUID, required)",
  "query_text": "string (required, the question to answer)",
  "selected_text": "string (optional, specific text selected by user)",
  "session_id": "string (optional, for tracking conversation context)"
}
```

**Response (200 OK, text/event-stream)**:
Streamed response with Server-Sent Events format:
```
data: {"chunk": "partial response text"}

data: {"chunk": "more response text"}

data: {"done": true, "final_response": "complete response"}
```

**Error Responses**:
- 400: Invalid request body
- 401: Unauthorized
- 404: Book not found
- 422: Validation error
- 500: Processing error

### 3. Query History

#### GET /history
Retrieve query history for a book or session.

**Query Parameters**:
- `book_id`: string (optional, filter by book)
- `session_id`: string (optional, filter by session)
- `limit`: integer (optional, default 10)
- `offset`: integer (optional, default 0)

**Response (200 OK)**:
```json
{
  "queries": [
    {
      "id": "string (UUID)",
      "book_id": "string (UUID)",
      "query_text": "string",
      "response_text": "string",
      "timestamp": "datetime",
      "accuracy_score": "float (optional)"
    }
  ],
  "total": "integer"
}
```

**Error Responses**:
- 401: Unauthorized

#### POST /history/{query_id}/feedback
Submit feedback for a query response.

**Request Body**:
```json
{
  "accuracy_score": "float (0-1, optional)",
  "feedback_text": "string (optional)"
}
```

**Response (200 OK)**:
```json
{
  "message": "Feedback submitted successfully"
}
```

**Error Responses**:
- 400: Invalid request body
- 401: Unauthorized
- 404: Query not found
- 422: Validation error

### 4. Health and Status

#### GET /health
Check the health status of the API.

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "timestamp": "datetime",
  "dependencies": {
    "cohere": "connected|disconnected",
    "qdrant": "connected|disconnected",
    "postgres": "connected|disconnected"
  }
}
```

#### GET /status
Get detailed status information.

**Response (200 OK)**:
```json
{
  "status": "string",
  "version": "string",
  "uptime": "integer (seconds)",
  "active_users": "integer",
  "queries_processed": "integer",
  "timestamp": "datetime"
}
```

## Error Format
All error responses follow this format:
```json
{
  "error": {
    "code": "string (error code)",
    "message": "string (human-readable error message)",
    "details": "object (optional, additional error details)"
  }
}
```

## Common Error Codes
- `AUTH_ERROR`: Authentication failed
- `VALIDATION_ERROR`: Request validation failed
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `PROCESSING_ERROR`: Error during request processing
- `RATE_LIMIT_EXCEEDED`: Rate limit exceeded
- `SERVICE_UNAVAILABLE`: External service unavailable