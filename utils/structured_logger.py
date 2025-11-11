"""
Sistema de logging estructurado
"""
import logging
import json
from datetime import datetime
from typing import Dict, Any

class StructuredLogger:
    """Logger con formato estructurado para mejor análisis"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Configura el logger con formato JSON"""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_event(self, event_type: str, data: Dict[str, Any], level: str = "INFO"):
        """Registra evento estructurado"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        }
        
        message = json.dumps(log_entry, ensure_ascii=False)
        
        if level == "ERROR":
            self.logger.error(message)
        elif level == "WARNING":
            self.logger.warning(message)
        else:
            self.logger.info(message)
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Registra evento de seguridad"""
        self.log_event(f"SECURITY_{event_type}", details, "WARNING")
    
    def log_processing_event(self, pdf_file: str, event: str, details: Dict[str, Any] = None):
        """Registra evento de procesamiento"""
        data = {'pdf_file': pdf_file, 'event': event}
        if details:
            data.update(details)
        self.log_event("PROCESSING", data)