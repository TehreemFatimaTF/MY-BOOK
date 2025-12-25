# Quickstart Guide: Book RAG Chatbot

**Feature**: 001-book-rag-chatbot
**Date**: 2025-12-24

## Overview
This guide provides instructions for quickly setting up and running the Book RAG Chatbot for development and testing purposes.

## Prerequisites
- Python 3.11+
- pip package manager
- Git
- Cohere API key
- Qdrant API key and cluster endpoint
- Neon Postgres database connection string

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following variables:

```env
COHERE_API_KEY=xzwpz0gbkUMQl3Z9V1gfPQlOPDVk7WVLaggg0wbp
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.mylOODSXs7r7X9I5tmD3TPzkygNC7ETuXFbJ3TqnHMo
QDRANT_CLUSTER_ENDPOINT=https://93fcb6e7-a4b3-4a43-8672-29f49b7dca47.europe-west3-0.gcp.cloud.qdrant.io
NEON_DB_URL='postgresql://neondb_owner:npg_XKh79jmJaPTy@ep-dry-shape-adaugw9x-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
```

### 5. Initialize the Database
```bash
cd backend/src
python -m utils.init_db
```

### 6. Run the Application
```bash
cd backend/src
python -m api.main
```

The application will start on `http://localhost:8000` by default.

## Basic Usage

### 1. Upload a Book
```bash
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample Book",
    "author": "Author Name",
    "content": "Full content of the book..."
  }'
```

### 2. Query Book Content
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "<book-id>",
    "query_text": "What is this book about?"
  }'
```

### 3. Query Selected Text
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "<book-id>",
    "query_text": "Explain this concept",
    "selected_text": "The specific text the user has selected..."
  }'
```

## Development Workflow

### Running Tests
```bash
cd backend
python -m pytest tests/
```

### Running with Qwen CLI for Prototyping
```bash
qwen run backend/src/api/main.py
```

### Building for Demo
```bash
# Build the backend
cd backend
python -m build

# Package for demo deployment
python -m packaging.package_demo
```

## Troubleshooting

### Common Issues
1. **API Keys Not Working**: Verify your API keys are correct and have the necessary permissions.
2. **Database Connection Issues**: Check that the Neon DB connection string is properly formatted.
3. **Qdrant Connection Issues**: Ensure the cluster endpoint is accessible and the API key is valid.

### Getting Help
- Check the logs in `backend/logs/`
- Run `python -m debugging.check_config` to validate your setup
- Refer to the full documentation in the `docs/` directory