"""
Módulo para detección y procesamiento de códigos QR
"""
import re
import numpy as np
from typing import List, Dict, Optional, Any
import logging

try:
    import cv2  # type: ignore
except ImportError:
    # Fallback si OpenCV no está disponible
    cv2 = None

try:
    from pyzbar.pyzbar import decode  # type: ignore
except ImportError:
    # Fallback si pyzbar no está disponible
    def decode(image):
        return []

# Importar configuración
from config import CERTIFICATE_PRESENT_VALUE

logger = logging.getLogger(__name__)


def advanced_qr_detection_memory(image: Any) -> List[str]:
    """
    Detección avanzada de QR con múltiples técnicas de procesamiento, en memoria
    
    Args:
        image: Imagen como array numpy
        
    Returns:
        Lista de datos QR decodificados
    """
    qr_codes_found = []
    
    try:
        if image is None or cv2 is None:
            logger.warning("OpenCV no disponible o imagen nula")
            return qr_codes_found
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Técnica 1: Imagen original en escala de grises
        qr_codes = decode(gray)
        qr_codes_found.extend([qr.data.decode('utf-8', errors='ignore') for qr in qr_codes])
        
        # Si ya encontramos QR, podemos parar aquí para optimizar
        if qr_codes_found:
            return list(set(qr_codes_found))
        
        # Técnica 2: Umbralización adaptativa
        try:
            adaptive_thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            qr_codes = decode(adaptive_thresh)
            qr_codes_found.extend([qr.data.decode('utf-8', errors='ignore') for qr in qr_codes])
            
            if qr_codes_found:
                return list(set(qr_codes_found))
        except cv2.error as e:
            logger.warning(f"Error en procesamiento OpenCV: {e}")
        except Exception as e:
            logger.error(f"Error inesperado en umbralización adaptativa: {e}")
        
        # Técnica 3: Umbralización binaria con diferentes valores
        # Valores de threshold para optimizar detección de QR
        THRESHOLD_VALUES = [100, 127, 150, 180, 200]
        for thresh_value in THRESHOLD_VALUES:
            try:
                _, binary_thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
                qr_codes = decode(binary_thresh)
                qr_codes_found.extend([qr.data.decode('utf-8', errors='ignore') for qr in qr_codes])
                
                if qr_codes_found:
                    return list(set(qr_codes_found))
            except cv2.error as e:
                logger.warning(f"Error en threshold {thresh_value}: {e}")
            except Exception as e:
                logger.error(f"Error inesperado en threshold {thresh_value}: {e}")
        
    except Exception as e:
        logger.error(f"Error en detección avanzada de QR: {e}")
    
    # Eliminar duplicados
    return list(set(qr_codes_found))


def enhanced_parse_qr_data(qr_data: str) -> Dict[str, str]:
    """
    Parseo mejorado de datos del QR con manejo robusto de errores
    
    Args:
        qr_data: Datos crudos del QR
        
    Returns:
        Diccionario con datos parseados
    """
    row = {'raw_data': qr_data}
    
    try:
        qr_data_clean = qr_data.strip().replace('\r', '\n')
        lines = [line.strip() for line in qr_data_clean.split('\n') if line.strip()]
        
        row.update({
            'nombre_alumno': '',
            'curp': '',
            'url': '',
            'promedio': '',
            'autoridad': '',
            'certificado': '',
            'año': '',
            'folio': ''
        })
        
        # Extraer URL con validación mejorada
        url_pattern = r'https?://[^\s<>"\']+|<a\s+href=[\'"](https?://[^"\']*)[\'"]'
        url_match = re.search(url_pattern, qr_data, re.IGNORECASE)
        if url_match:
            if url_match.groups() and url_match.group(1):
                row['url'] = url_match.group(1)
            else:
                row['url'] = url_match.group(0)
            
            # Extraer folio de la URL
            if row['url']:
                folio_match = re.search(r'/([a-f0-9\-]+)(?:\?.*)?$', row['url'])
                if folio_match:
                    row['folio'] = folio_match.group(1)
        
        # Función auxiliar para validar CURP
        def es_curp(cadena: str) -> bool:
            if not cadena:
                return False
            curp_pattern = r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]{2}$'
            return len(cadena) == 18 and bool(re.match(curp_pattern, cadena.upper()))
        
        def limpiar_linea(linea: str) -> str:
            return re.sub(r'^-\s*', '', linea.strip())
        
        # Parsing unificado - una sola pasada por las líneas
        for line in lines:
            line_clean = limpiar_linea(line)
            line_upper = line_clean.upper()
            
            if line_upper.startswith('ALUMNO:') and not row['nombre_alumno']:
                nombre_match = re.search(r'ALUMNO:\s*(.+)', line_clean, re.IGNORECASE)
                if nombre_match:
                    row['nombre_alumno'] = nombre_match.group(1).strip()
            
            elif line_upper.startswith('CURP') and 'ALUMNO' in line_upper and not row['curp']:
                curp_match = re.search(r'CURP[^:]*:\s*([A-Z0-9]+)', line_clean, re.IGNORECASE)
                if curp_match:
                    curp_candidate = curp_match.group(1).strip().upper()
                    if es_curp(curp_candidate):
                        row['curp'] = curp_candidate
            
            elif line_upper.startswith('PROMEDIO:') and not row['promedio']:
                promedio_match = re.search(r'promedio:\s*(\d+\.?\d*)', line_clean, re.IGNORECASE)
                if promedio_match:
                    row['promedio'] = promedio_match.group(1)
            
            elif line_upper.startswith('AUTORIDAD:') and not row['autoridad']:
                autoridad_match = re.search(r'autoridad:\s*(.+)', line_clean, re.IGNORECASE)
                if autoridad_match:
                    row['autoridad'] = autoridad_match.group(1).strip()
            
            elif line_upper.startswith('FOLIO:') and not row['folio']:
                folio_match = re.search(r'folio:\s*(.+)', line_clean, re.IGNORECASE)
                if folio_match:
                    row['folio'] = folio_match.group(1).strip()
            
            elif (line_upper == 'CERTIFICADO' or 'CERTIFICADO' in line_upper) and not row['certificado']:
                row['certificado'] = CERTIFICATE_PRESENT_VALUE
            
            elif re.match(r'^\d{4}-\d{4}$', line_clean) and not row['año']:
                row['año'] = line_clean
            
            elif re.match(r'^20\d{2}$', line_clean) and not row['año']:
                row['año'] = line_clean
            
            # Buscar CURP independiente y nombre sin prefijos
            elif not row['curp'] and es_curp(line_clean):
                row['curp'] = line_clean.upper()
            
            elif (not row['nombre_alumno'] and 
                  len(line_clean) > 10 and len(line_clean) < 80 and
                  not es_curp(line_clean) and
                  ':' not in line_clean and 
                  not re.search(r'https?://', line_clean, re.IGNORECASE) and
                  not re.match(r'^\d{4}(-\d{4})?$', line_clean) and
                  re.match(r'^[a-zA-ZáéíóúñÁÉÍÓÚÑ\s]+$', line_clean)):
                if not any(word in line_clean.upper() for word in ['CERTIFICADO', 'UNIVERSIDAD', 'SECRETARIA', 'INSTITUTO']):
                    row['nombre_alumno'] = line_clean
        
        if not row['certificado'] and (row['nombre_alumno'] or row['curp']):
            row['certificado'] = CERTIFICATE_PRESENT_VALUE
        
        # Corrección final: si nombre_alumno es en realidad un CURP
        if row['nombre_alumno'] and es_curp(row['nombre_alumno']):
            if not row['curp']:
                row['curp'] = row['nombre_alumno']
            row['nombre_alumno'] = ''
            
    except Exception as e:
        logger.error(f"Error al parsear datos del QR: {e}")
        row['error_parsing'] = str(e)
    
    return row
