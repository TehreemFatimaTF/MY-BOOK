"""
API key authentication middleware with rate limiting
"""
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.config.settings import settings
from src.utils.logging import logger, log_security_event
from src.utils.error_handling import check_rate_limit, RateLimitExceededError
import time
import hashlib

class APIKeyAuth:
    def __init__(self):
        # In a real implementation, we would validate the API key against a database or other storage
        # For now, we'll just check if it matches the expected format
        self.valid_api_key = settings.cohere_api_key  # Using Cohere API key as example; in practice, you'd have a separate key for API access

    async def __call__(self, request: Request) -> bool:
        # Extract the API key from the Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Missing or invalid Authorization header")
            log_security_event(
                event_type="UNAUTHORIZED_ACCESS_ATTEMPT",
                severity="MEDIUM",
                description="Request missing or invalid Authorization header",
                ip_address=request.client.host if request.client else None
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header"
            )

        api_key = auth_header[7:]  # Remove "Bearer " prefix

        # In a real implementation, you would validate the API key against a database
        # For this example, we'll just check if it's not empty
        if not api_key or len(api_key) < 10:  # Basic validation
            logger.warning("Invalid API key format")
            log_security_event(
                event_type="INVALID_API_KEY",
                severity="HIGH",
                description="Request with invalid API key format",
                ip_address=request.client.host if request.client else None
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )

        # Check rate limiting (100 requests per hour per API key)
        api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        if not check_rate_limit(api_key_hash, limit=100, window=3600):
            logger.warning(f"Rate limit exceeded for API key: {api_key_hash[:10]}...")
            log_security_event(
                event_type="RATE_LIMIT_EXCEEDED",
                severity="MEDIUM",
                description=f"Rate limit exceeded for API key: {api_key_hash[:10]}...",
                user_id=api_key_hash,
                ip_address=request.client.host if request.client else None
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )

        # Add the API key to the request state for later use
        request.state.api_key = api_key
        request.state.api_key_hash = api_key_hash

        # Log the API call
        start_time = time.time()
        request.state.start_time = start_time

        # Continue with the request
        return True

# Initialize the authentication middleware
api_key_auth = APIKeyAuth()