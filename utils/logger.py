"""
Sistema de logging personalizado para el proyecto
"""
import os
import logging
from datetime import datetime
from typing import Optional
from utils.security_validator import SecurityValidator

logger = logging.getLogger(__name__)

class ProcessLogger:
    """Logger dedicado para el proceso de extracción y validación"""
    
    def __init__(self, log_file: Optional[str] = None):
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"logs/process_log_{timestamp}.txt"
        
        # VALIDACIÓN DE SEGURIDAD - Prevenir path traversal
        try:
            # Usar safe_join_path para prevenir path traversal
            safe_log_file = SecurityValidator.safe_join_path(
                os.path.join(os.getcwd(), "build", "logs"), 
                os.path.basename(log_file)
            )
            log_file = safe_log_file
        except ValueError as e:
            logger.error(f"Path de log inseguro: {e}")
            self.log_file = None
            return
        except Exception as e:
            logger.error(f"Error validando path de log: {e}")
            self.log_file = None
            return
        
        self.log_file = log_file
        
        # Crear directorio de logs si no existe
        try:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        except (OSError, PermissionError) as e:
            logger.error(f"No se pudo crear directorio de logs: {e}")
            self.log_file = None
            return
        
        # Crear archivo de log
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(f"INICIO DEL PROCESO: {datetime.now().isoformat()}\n")
                f.write("="*60 + "\n\n")
        except FileNotFoundError as e:
            logger.error(f"Directorio de log no encontrado: {e}")
            self.log_file = None
        except PermissionError as e:
            logger.error(f"Sin permisos para crear archivo de log: {e}")
            self.log_file = None
        except OSError as e:
            logger.error(f"Error del sistema creando log: {e}")
            self.log_file = None
        except Exception as e:
            logger.error(f"Error inesperado creando log: {e}")
            self.log_file = None
    
    def log(self, message: str):
        """Registra un mensaje con timestamp"""
        if self.log_file is None:
            return
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {message}\n")
        except FileNotFoundError as e:
            logger.warning(f"Archivo de log no encontrado: {e}")
        except PermissionError as e:
            logger.warning(f"Sin permisos para escribir log: {e}")
        except OSError as e:
            logger.warning(f"Error del sistema escribiendo log: {e}")
        except UnicodeEncodeError as e:
            logger.warning(f"Error de codificación en log: {e}")
        except Exception as e:
            logger.error(f"Error inesperado en log: {e}")
