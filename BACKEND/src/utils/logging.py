"""
Error handling and logging infrastructure
"""
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from typing import Optional
import json

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
def setup_logging():
    # Create logger
    logger = logging.getLogger('book_rag_chatbot')
    logger.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=1024*1024*10,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Initialize logger
logger = setup_logging()

class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "APP_ERROR"
        self.details = details or {}
        logger.error(f"{self.error_code}: {message} - Details: {details}")

class ValidationError(AppException):
    """Validation error"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, "VALIDATION_ERROR", details)

class ProcessingError(AppException):
    """Processing error"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, "PROCESSING_ERROR", details)

class ResourceNotFoundError(AppException):
    """Resource not found error"""
    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} with ID {resource_id} not found"
        details = {"resource_type": resource_type, "resource_id": resource_id}
        super().__init__(message, "RESOURCE_NOT_FOUND", details)

class ExternalServiceError(AppException):
    """External service error"""
    def __init__(self, service_name: str, message: str):
        details = {"service": service_name, "message": message}
        super().__init__(f"Error communicating with {service_name}: {message}", "EXTERNAL_SERVICE_ERROR", details)

def log_api_call(endpoint: str, method: str, user_id: Optional[str] = None, duration: Optional[float] = None):
    """Log API calls"""
    log_data = {
        "type": "api_call",
        "endpoint": endpoint,
        "method": method,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "duration_ms": duration * 1000 if duration else None
    }
    logger.info(json.dumps(log_data))

def log_query_execution(query_id: str, book_id: str, query_text: str, response_length: int):
    """Log query execution details"""
    log_data = {
        "type": "query_execution",
        "query_id": query_id,
        "book_id": book_id,
        "query_text_preview": query_text[:100] + "..." if len(query_text) > 100 else query_text,
        "response_length": response_length,
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.info(json.dumps(log_data))

def log_error(error: Exception, context: Optional[dict] = None):
    """Log error with context"""
    log_data = {
        "type": "error",
        "error_type": type(error).__name__,
        "message": str(error),
        "context": context,
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.error(json.dumps(log_data))

def log_user_story_1_operation(operation: str, book_id: str, details: Optional[dict] = None):
    """Log specific operations for User Story 1 (Query Book Content)"""
    log_data = {
        "type": "user_story_1_operation",
        "operation": operation,
        "book_id": book_id,
        "details": details or {},
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.info(json.dumps(log_data))

def log_query_processing(query_id: str, book_id: str, query_text: str, response_time: Optional[float] = None):
    """Log query processing events"""
    log_data = {
        "type": "query_processing",
        "query_id": query_id,
        "book_id": book_id,
        "query_text_preview": query_text[:100] + "..." if len(query_text) > 100 else query_text,
        "response_time_ms": response_time * 1000 if response_time else None,
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.info(json.dumps(log_data))

def log_selected_text_operation(operation: str, query_id: str, book_id: str, selected_text_preview: str, details: Optional[dict] = None):
    """Log specific operations for selected text functionality"""
    log_data = {
        "type": "selected_text_operation",
        "operation": operation,
        "query_id": query_id,
        "book_id": book_id,
        "selected_text_preview": selected_text_preview[:100] + "..." if len(selected_text_preview) > 100 else selected_text_preview,
        "details": details or {},
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.info(json.dumps(log_data))

def log_system_metrics(cpu_percent: float, memory_percent: float, active_connections: int, queries_per_second: float):
    """Log system metrics for observability"""
    log_data = {
        "type": "system_metrics",
        "cpu_percent": cpu_percent,
        "memory_percent": memory_percent,
        "active_connections": active_connections,
        "queries_per_second": queries_per_second,
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.info(json.dumps(log_data))

def log_user_action(user_id: str, action: str, resource: str, metadata: Optional[dict] = None):
    """Log user actions for audit and analytics"""
    log_data = {
        "type": "user_action",
        "user_id": user_id,
        "action": action,
        "resource": resource,
        "metadata": metadata or {},
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.info(json.dumps(log_data))

def log_performance_metric(metric_name: str, value: float, unit: str, tags: Optional[dict] = None):
    """Log performance metrics for monitoring"""
    log_data = {
        "type": "performance_metric",
        "metric_name": metric_name,
        "value": value,
        "unit": unit,
        "tags": tags or {},
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.info(json.dumps(log_data))

def log_security_event(event_type: str, severity: str, description: str, user_id: Optional[str] = None, ip_address: Optional[str] = None):
    """Log security-related events"""
    log_data = {
        "type": "security_event",
        "event_type": event_type,
        "severity": severity,
        "description": description,
        "user_id": user_id,
        "ip_address": ip_address,
        "timestamp": datetime.utcnow().isoformat()
    }
    logger.warning(json.dumps(log_data))  # Use warning level for security events