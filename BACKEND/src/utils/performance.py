"""
Performance monitoring and optimization utilities
"""
import time
import asyncio
from typing import Callable, Any
from functools import wraps
from src.utils.logging import logger
import statistics

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def measure_time(self, name: str = None):
        """
        Decorator to measure execution time of functions
        """
        def decorator(func: Callable) -> Callable:
            nonlocal name
            if name is None:
                name = func.__name__
            
            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    duration = end_time - start_time
                    self._record_metric(name, duration)
                    logger.info(f"{name} executed in {duration:.4f} seconds")
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs) -> Any:
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    duration = end_time - start_time
                    self._record_metric(name, duration)
                    logger.info(f"{name} executed in {duration:.4f} seconds")
            
            # Return the appropriate wrapper based on function type
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator
    
    def _record_metric(self, name: str, value: float):
        """
        Record a performance metric
        """
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)
    
    def get_stats(self, name: str) -> dict:
        """
        Get statistics for a specific metric
        """
        if name not in self.metrics or not self.metrics[name]:
            return {}
        
        values = self.metrics[name]
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": statistics.mean(values),
            "median": statistics.median(values),
            "p95": self._percentile(values, 95),
            "p99": self._percentile(values, 99)
        }
    
    def _percentile(self, data: list, percentile: float) -> float:
        """
        Calculate percentile of a list of values
        """
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower_index = int(index)
            upper_index = lower_index + 1
            weight = index - lower_index
            return sorted_data[lower_index] * (1 - weight) + sorted_data[upper_index] * weight
    
    def reset_metrics(self):
        """
        Reset all collected metrics
        """
        self.metrics = {}

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

# Predefined performance checks
def check_response_time(response_time: float, threshold: float = 3.0) -> bool:
    """
    Check if response time is within acceptable threshold
    """
    return response_time <= threshold

def check_throughput(requests_per_second: float, target: float = 10.0) -> bool:
    """
    Check if throughput meets target
    """
    return requests_per_second >= target

def log_performance_metrics():
    """
    Log key performance metrics
    """
    for metric_name in performance_monitor.metrics:
        stats = performance_monitor.get_stats(metric_name)
        if stats:
            logger.info(f"Performance stats for {metric_name}: {stats}")