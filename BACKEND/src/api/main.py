"""
Main FastAPI application with routing and middleware structure
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import book_routes, query_routes, history_routes
from src.api.translation_routes import router as translation_router
from src.config.settings import settings
# --- YEH LINE ADD KAREIN ---
from src.db.postgres_client import postgres_client
import uvicorn
import os
from datetime import datetime

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Create the FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="RAG Chatbot for Embedded Book Interaction",
    version=settings.app_version,
    debug=settings.debug
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"VALIDATION ERROR: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

# --- YEH STARTUP AUR SHUTDOWN LOGIC ADD KAREIN ---
@app.on_event("startup")
async def startup_event():
    """Server start hote waqt database pool initialize karega"""
    await postgres_client.initialize_pool()

@app.on_event("shutdown")
async def shutdown_event():
    """Server band hote waqt database pool close karega"""
    await postgres_client.close_pool()
# -----------------------------------------------

# Add CORS middleware
# main.py mein CORSMiddleware wala section aise update karein:

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development ke liye sab allow kar dein
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS sab allow ho jayenge
    allow_headers=["*"],
)
# Include API routes
app.include_router(book_routes.router, prefix=settings.api_v1_prefix)
app.include_router(query_routes.router, prefix=settings.api_v1_prefix)
app.include_router(history_routes.router, prefix=settings.api_v1_prefix)
app.include_router(translation_router, prefix=settings.api_v1_prefix)

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
