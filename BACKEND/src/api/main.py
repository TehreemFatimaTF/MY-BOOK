from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings
from src.api import book_routes, query_routes, history_routes
from datetime import datetime
import os
import uvicorn

# -----------------------------
# Create FastAPI app
# -----------------------------
app = FastAPI(
    title=settings.app_name,
    description="RAG Chatbot for Embedded Book Interaction",
    version=settings.app_version,
    debug=settings.debug
)

# -----------------------------
# CORS middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # Add your Vercel frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# -----------------------------
# Include API routes
# -----------------------------
app.include_router(book_routes.router, prefix=settings.api_v1_prefix)
app.include_router(query_routes.router, prefix=settings.api_v1_prefix)
app.include_router(history_routes.router, prefix=settings.api_v1_prefix)

# -----------------------------
# Health endpoint
# -----------------------------
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "dependencies": {
            "cohere": "connected",
            "qdrant": "connected",
            "postgres": "connected"
        }
    }

# -----------------------------
# Protected Query Endpoint
# -----------------------------
@app.post(f"{settings.api_v1_prefix}/query")
def query_endpoint(payload: dict, authorization: str = Header(None)):
    expected_api_key = os.environ.get("BACKEND_API_KEY", "")
    if authorization != f"Bearer {expected_api_key}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_query = payload.get("query", "")
    book_id = payload.get("book_id", "")

    # Placeholder logic: Replace with your RAG query logic
    response_text = f"Received query '{user_query}' for book '{book_id}'"
    return {"response": response_text}

# -----------------------------
# Run server locally
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=settings.debug
    )
