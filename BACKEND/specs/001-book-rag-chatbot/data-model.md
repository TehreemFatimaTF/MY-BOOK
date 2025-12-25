# Data Model: Book RAG Chatbot

**Feature**: 001-book-rag-chatbot
**Date**: 2025-12-24

## Overview
This document defines the data models for the Book RAG Chatbot feature, including entities, attributes, relationships, and validation rules.

## Entity: Book Content
**Description**: Represents the text and metadata of a book that will be indexed for RAG queries

**Attributes**:
- `id` (UUID, required): Unique identifier for the book
- `title` (String, required): Title of the book
- `author` (String, required): Author of the book
- `isbn` (String, optional): ISBN of the book
- `content` (Text, required): Full text content of the book
- `content_hash` (String, required): Hash of the content for change detection
- `chunked_content` (JSON, optional): Content split into searchable chunks
- `created_at` (DateTime, required): Timestamp when the book was added
- `updated_at` (DateTime, required): Timestamp when the book was last updated

**Relationships**:
- One-to-many with Query History (one book can have many queries)

## Entity: User Query
**Description**: Represents a question or request from the user that needs to be processed against book content

**Attributes**:
- `id` (UUID, required): Unique identifier for the query
- `book_id` (UUID, required): Reference to the book being queried
- `query_text` (String, required): The text of the user's query
- `query_embedding` (Array<Float>, optional): Vector embedding of the query
- `selected_text` (String, optional): Text selected by user for focused queries
- `created_at` (DateTime, required): Timestamp when the query was made
- `session_id` (String, optional): Session identifier for grouping related queries

**Relationships**:
- Many-to-one with Book Content (many queries for one book)
- One-to-many with Retrieved Context (one query can retrieve multiple contexts)

## Entity: Retrieved Context
**Description**: Represents the relevant portions of book content retrieved based on the user query

**Attributes**:
- `id` (UUID, required): Unique identifier for the retrieved context
- `query_id` (UUID, required): Reference to the original query
- `content_chunk` (Text, required): The text chunk retrieved from the book
- `chunk_id` (String, required): Identifier for the specific chunk in the book
- `relevance_score` (Float, required): Score indicating relevance to the query
- `retrieved_at` (DateTime, required): Timestamp when the context was retrieved

**Relationships**:
- Many-to-one with User Query (many contexts retrieved for one query)
- Many-to-one with Book Content (contexts come from one book)

## Entity: Generated Response
**Description**: Represents the AI-generated answer to the user's query based on the retrieved context

**Attributes**:
- `id` (UUID, required): Unique identifier for the response
- `query_id` (UUID, required): Reference to the original query
- `response_text` (Text, required): The text of the AI-generated response
- `confidence_score` (Float, optional): Confidence level in the response
- `generated_at` (DateTime, required): Timestamp when the response was generated
- `source_chunks` (Array<String>, optional): IDs of the chunks used to generate the response

**Relationships**:
- Many-to-one with User Query (many responses possible for one query, though typically one)
- One-to-many with Retrieved Context (response based on multiple contexts)

## Entity: User Selection
**Description**: Represents the specific text selected by the user for focused queries

**Attributes**:
- `id` (UUID, required): Unique identifier for the selection
- `query_id` (UUID, required): Reference to the associated query
- `selected_text` (Text, required): The text selected by the user
- `selection_metadata` (JSON, optional): Additional metadata about the selection (position, length, etc.)
- `created_at` (DateTime, required): Timestamp when the selection was made

**Relationships**:
- Many-to-one with User Query (many selections can be made for one query)

## Entity: Query History
**Description**: Stores historical information about user queries and responses for analytics

**Attributes**:
- `id` (UUID, required): Unique identifier for the history record
- `query_id` (UUID, required): Reference to the original query
- `user_id` (String, optional): Identifier for the user (if available)
- `query_text` (String, required): The original query text
- `response_text` (Text, required): The AI-generated response
- `accuracy_score` (Float, optional): Accuracy rating of the response
- `feedback` (Text, optional): User feedback on the response
- `timestamp` (DateTime, required): When the query was made

**Relationships**:
- Many-to-one with Book Content (queries are for specific books)

## Validation Rules

1. **Book Content**:
   - Title and author must not be empty
   - Content must be at least 100 characters
   - Content hash must be unique to prevent duplicates

2. **User Query**:
   - Query text must be at least 3 characters
   - Must reference a valid book
   - Selected text (if provided) must be part of the referenced book

3. **Retrieved Context**:
   - Relevance score must be between 0 and 1
   - Content chunk must not be empty

4. **Generated Response**:
   - Response text must not be empty
   - Confidence score (if provided) must be between 0 and 1

5. **User Selection**:
   - Selected text must not be empty
   - Must be a substring of the referenced book content

## State Transitions

1. **Query Processing Flow**:
   - User Query (Created) → Retrieved Context (Retrieved) → Generated Response (Generated) → Query History (Logged)

2. **Book Content States**:
   - Book Content (Added) → Content Processed (Chunks Created) → Indexed (Available for Queries)