"""
Main FastAPI application with routing and middleware structure
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import book_routes, query_routes, history_routes
from src.config.settings import settings
import uvicorn
import os
from datetime import datetime

# Create the FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="RAG Chatbot for Embedded Book Interaction",
    version=settings.app_version,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # Allow credentials to be sent with cross-origin requests
    allow_credentials=True,
    # Allow all origins during development, restrict in production
    allow_origins=["https://my-book-phi-nine.vercel.app/"] if settings.debug else settings.allowed_origins,
    # Allow all methods and headers
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers that browsers can access
    expose_headers=["Access-Control-Allow-Origin"]
)

# Include API routes
app.include_router(book_routes.router, prefix=settings.api_v1_prefix)
app.include_router(query_routes.router, prefix=settings.api_v1_prefix)
app.include_router(history_routes.router, prefix=settings.api_v1_prefix)

# Add a health check endpoint
@app.get("/")
def read_root():
    return {"status": "healthy", "app": settings.app_name, "version": settings.app_version}

@app.get("/health")
def health_check():
    # In a real implementation, we would check actual connectivity to each service
    # For now, we'll return a basic health status
    import time
    timestamp = time.time()

    # In a real implementation, we would check:
    # - Cohere API connectivity
    # - Qdrant connectivity
    # - PostgreSQL connectivity
    # For this example, we'll assume all are connected

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "dependencies": {
            "cohere": "connected",  # This would be checked in real implementation
            "qdrant": "connected",  # This would be checked in real implementation
            "postgres": "connected"  # This would be checked in real implementation
        }
    }

@app.get("/status")
def status_check():
    """Get detailed status information"""
    import os
    import psutil
    from datetime import datetime, timedelta

    # Get process info
    process = psutil.Process(os.getpid())

    return {
        "status": "running",
        "version": settings.app_version,
        "uptime": "0",  # Would be calculated based on app start time
        "active_users": 0,  # Would be tracked in a real implementation
        "queries_processed": 0,  # Would be tracked in a real implementation
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_mb": round(process.memory_info().rss / 1024 / 1024, 2),
            "process_count": len(psutil.pids())
        }
    }

if __name__ == "__main__":
    # This would be run with uvicorn in production
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True if settings.debug else False
    )
