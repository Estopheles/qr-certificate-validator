#!/usr/bin/env python3
"""
Decorador para monitorear rendimiento de funciones específicas
"""
import time
import functools
from typing import Callable, Any
import psutil

from utils.structured_logger import StructuredLogger


def monitor_performance(log_results: bool = True):
    """
    Decorador para monitorear rendimiento de funciones
    
    Args:
        log_results: Si loggear los resultados automáticamente
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Métricas iniciales
            start_time = time.time()
            process = psutil.Process()
            
            initial_cpu = process.cpu_percent()
            initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
            
            # Ejecutar función
            try:
                result = func(*args, **kwargs)
                success = True
                error = None
            except Exception as e:
                result = None
                success = False
                error = str(e)
                raise
            finally:
                # Métricas finales
                end_time = time.time()
                execution_time = end_time - start_time
                
                final_cpu = process.cpu_percent()
                final_memory = process.memory_info().rss / (1024 * 1024)  # MB
                
                memory_delta = final_memory - initial_memory
                
                # Loggear si está habilitado
                if log_results:
                    logger = StructuredLogger(func.__module__)
                    logger.log_processing_event(
                        func.__name__,
                        "PERFORMANCE_METRICS",
                        {
                            "execution_time_seconds": round(execution_time, 3),
                            "cpu_percent": round(final_cpu, 2),
                            "memory_mb": round(final_memory, 2),
                            "memory_delta_mb": round(memory_delta, 2),
                            "success": success,
                            "error": error
                        }
                    )
            
            return result
        return wrapper
    return decorator


def monitor_critical_function(func: Callable) -> Callable:
    """Decorador simplificado para funciones críticas"""
    return monitor_performance(log_results=True)(func)