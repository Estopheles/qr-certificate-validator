"""
Módulo de validación de seguridad
"""
import os
import re
import ipaddress
import urllib.parse
from pathlib import Path
from typing import Set, Optional, Dict
import logging

logger = logging.getLogger(__name__)

class SecurityValidator:
    """Validador de seguridad centralizado"""
    
    # Dominios oficiales aprobados
    ALLOWED_DOMAINS: Set[str] = {
        'siged.sep.gob.mx',
        'www.siged.sep.gob.mx'
    }
    
    # Dominios de otros estados (requieren revisión manual)
    STATE_DOMAINS: Set[str] = {
        'certificados.edomex.gob.mx',
        'validacion.jalisco.gob.mx', 
        'certificados.nl.gob.mx'
    }
    
    # Patrones sospechosos de fraude
    SUSPICIOUS_PATTERNS: Set[str] = {
        '.gob.uk',  # Dominio incorrecto
        '.gov.com', # Dominio falso
        '.sep.com', # Dominio falso
        'siged.com' # Dominio falso
    }
    
    ALLOWED_FILE_EXTENSIONS: Set[str] = {
        '.pdf', '.xlsx', '.csv', '.json', '.txt', '.log', '.png'
    }
    
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    @staticmethod
    def validate_file_path(file_path: str, base_dir: str) -> bool:
        """Valida que el archivo esté en directorio permitido"""
        try:
            base_path = Path(base_dir).resolve()
            target_path = Path(file_path).resolve()
            
            # Verificar que esté dentro del directorio base
            if not target_path.is_relative_to(base_path):
                logger.warning(f"Path fuera de directorio: {file_path}")
                return False
            
            # Verificar extensión
            if target_path.suffix.lower() not in SecurityValidator.ALLOWED_FILE_EXTENSIONS:
                logger.warning(f"Extensión no permitida: {target_path.suffix}")
                return False
            
            # Verificar tamaño si existe
            if target_path.exists() and target_path.stat().st_size > SecurityValidator.MAX_FILE_SIZE:
                logger.warning(f"Archivo muy grande: {file_path}")
                return False
            
            return True
        except (OSError, ValueError) as e:
            logger.error(f"Error validando path {file_path}: {e}")
            return False
    
    @staticmethod
    def validate_url(url: str) -> Dict[str, any]:
        """Valida URL y clasifica el tipo de dominio"""
        try:
            parsed = urllib.parse.urlparse(url)
            
            # Verificar esquema
            if parsed.scheme not in ('http', 'https'):
                return {'valid': False, 'reason': 'Esquema no válido', 'classification': 'INVALID'}
            
            domain = parsed.netloc.lower()
            
            # Verificar que no sea IP privada
            if SecurityValidator._is_private_ip(domain):
                logger.warning(f"IP privada detectada: {domain}")
                return {'valid': False, 'reason': 'IP privada', 'classification': 'SUSPICIOUS'}
            
            # Verificar patrones sospechosos (FRAUDE)
            for pattern in SecurityValidator.SUSPICIOUS_PATTERNS:
                if pattern in domain:
                    logger.error(f"POSIBLE FRAUDE detectado: {domain} contiene {pattern}")
                    return {'valid': False, 'reason': f'Patrón sospechoso: {pattern}', 'classification': 'FRAUD'}
            
            # Verificar dominios oficiales aprobados
            if domain in SecurityValidator.ALLOWED_DOMAINS:
                return {'valid': True, 'reason': 'Dominio oficial aprobado', 'classification': 'OFFICIAL'}
            
            # Verificar dominios de otros estados
            if domain in SecurityValidator.STATE_DOMAINS:
                logger.warning(f"Dominio de otro estado detectado: {domain}")
                return {'valid': False, 'reason': 'Dominio de otro estado', 'classification': 'OTHER_STATE'}
            
            # Dominio desconocido
            logger.warning(f"Dominio desconocido: {domain}")
            return {'valid': False, 'reason': 'Dominio no reconocido', 'classification': 'UNKNOWN'}
            
        except Exception as e:
            logger.error(f"Error validando URL {url}: {e}")
            return {'valid': False, 'reason': f'Error de validación: {e}', 'classification': 'ERROR'}
    
    @staticmethod
    def _is_private_ip(hostname: str) -> bool:
        """Verifica si es una IP privada"""
        try:
            ip = ipaddress.ip_address(hostname)
            return ip.is_private or ip.is_loopback or ip.is_link_local
        except ValueError:
            return False
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitiza nombre de archivo removiendo caracteres peligrosos"""
        if not filename:
            return "unnamed_file"
            
        # Remover caracteres peligrosos
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        safe_name = safe_name.strip('. ')
        
        # Verificar nombres reservados de Windows
        safe_name = SecurityValidator._handle_reserved_names(safe_name)
        
        # Limitar longitud del nombre
        return safe_name[:255]
    
    @staticmethod
    def _handle_reserved_names(filename: str) -> str:
        """Maneja nombres reservados de Windows"""
        reserved_names = {
            'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 
            'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 
            'LPT7', 'LPT8', 'LPT9'
        }
        
        name_parts = filename.split('.')
        if name_parts and name_parts[0].upper() in reserved_names:
            name_parts[0] = f"file_{name_parts[0]}"
            return '.'.join(name_parts)
            
        return filename
    
    @staticmethod
    def safe_join_path(base_dir: str, filename: str) -> str:
        """Une paths de forma segura"""
        # Sanitizar nombre de archivo
        safe_filename = SecurityValidator.sanitize_filename(os.path.basename(filename))
        if not safe_filename or safe_filename in ('.', '..'):
            raise ValueError("Nombre de archivo inválido")
        
        full_path = os.path.join(base_dir, safe_filename)
        
        if not SecurityValidator.validate_file_path(full_path, base_dir):
            raise ValueError("Path fuera del directorio permitido")
        
        return full_path