"""
Comprehensive error handling and graceful degradation
"""
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.utils.logging import logger, log_error
import traceback
from typing import Optional, Dict, Any
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: Dict[str, Any]

# Custom exception classes
class AppBaseException(Exception):
    """Base application exception"""
    def __init__(self, message: str, error_code: str = "APP_ERROR", details: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class ConfigurationError(AppBaseException):
    """Raised when there's a configuration issue"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "CONFIG_ERROR", details)

class ExternalServiceError(AppBaseException):
    """Raised when an external service is unavailable"""
    def __init__(self, service_name: str, message: str):
        details = {"service": service_name}
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", details)

class RateLimitExceededError(AppBaseException):
    """Raised when rate limit is exceeded"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, "RATE_LIMIT_EXCEEDED")

# Global rate limiting storage (in production, use Redis or similar)
rate_limit_storage = {}

def setup_error_handlers(app: FastAPI):
    """
    Setup comprehensive error handlers for the application
    """
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions"""
        error_response = {
            "error": {
                "code": exc.status_code,
                "message": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
                "type": "HTTP_ERROR"
            }
        }
        
        # Log the error
        log_error(exc, {"path": request.url.path, "method": request.method})
        
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors"""
        error_details = []
        for error in exc.errors():
            error_details.append({
                "loc": error["loc"],
                "msg": error["msg"],
                "type": error["type"]
            })
        
        error_response = {
            "error": {
                "code": 422,
                "message": "Validation error",
                "type": "VALIDATION_ERROR",
                "details": error_details
            }
        }
        
        # Log the error
        log_error(exc, {"path": request.url.path, "method": request.method})
        
        return JSONResponse(
            status_code=422,
            content=error_response
        )
    
    @app.exception_handler(AppBaseException)
    async def app_exception_handler(request: Request, exc: AppBaseException):
        """Handle custom application exceptions"""
        error_response = {
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "type": exc.__class__.__name__,
                "details": exc.details
            }
        }
        
        # Log the error
        log_error(exc, {"path": request.url.path, "method": request.method})
        
        status_code = 500
        if exc.error_code == "EXTERNAL_SERVICE_ERROR":
            status_code = 503  # Service Unavailable
        elif exc.error_code == "RATE_LIMIT_EXCEEDED":
            status_code = 429  # Too Many Requests
        elif exc.error_code == "CONFIG_ERROR":
            status_code = 500
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other exceptions"""
        error_response = {
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
                "type": "INTERNAL_ERROR",
                "details": {
                    "path": request.url.path,
                    "method": request.method
                }
            }
        }
        
        # Log the full error with traceback
        logger.error(f"Internal error: {exc}\n{traceback.format_exc()}")
        log_error(exc, {"path": request.url.path, "method": request.method, "traceback": traceback.format_exc()})
        
        return JSONResponse(
            status_code=500,
            content=error_response
        )

def check_rate_limit(identifier: str, limit: int = 100, window: int = 3600) -> bool:
    """
    Simple rate limiting function
    In production, use Redis or similar for distributed rate limiting
    """
    import time
    
    current_time = time.time()
    
    if identifier not in rate_limit_storage:
        rate_limit_storage[identifier] = {"count": 1, "window_start": current_time}
        return True
    
    # Clean up old entries
    if current_time - rate_limit_storage[identifier]["window_start"] > window:
        rate_limit_storage[identifier] = {"count": 1, "window_start": current_time}
        return True
    
    # Check if limit exceeded
    if rate_limit_storage[identifier]["count"] >= limit:
        return False
    
    # Increment count
    rate_limit_storage[identifier]["count"] += 1
    return True

def graceful_degradation_handler(service_name: str, fallback_function=None):
    """
    Decorator to handle service failures gracefully
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ExternalServiceError as e:
                logger.warning(f"External service {service_name} failed: {e.message}. Attempting fallback.")
                
                if fallback_function:
                    try:
                        return fallback_function(*args, **kwargs)
                    except Exception as fallback_error:
                        logger.error(f"Fallback function also failed: {fallback_error}")
                        raise e
                else:
                    # If no fallback is provided, return a degraded response
                    return {
                        "status": "degraded",
                        "message": f"Service {service_name} is temporarily unavailable, using cached or default response",
                        "data": None
                    }
        return wrapper
    return decorator

# Example usage of graceful degradation
def fallback_search(*args, **kwargs):
    """Fallback search function when primary search fails"""
    return {
        "results": [],
        "message": "Search service temporarily unavailable, please try again later",
        "fallback_used": True
    }