"""
Módulo de validación de certificados
"""
import re
import logging
from typing import Dict

logger = logging.getLogger(__name__)


def validate_certificate_data(qr_data: Dict, web_data: Dict) -> Dict[str, str]:
    """
    Compara los datos del QR con los del sitio web con manejo mejorado de formatos
    
    Args:
        qr_data: Datos extraídos del QR
        web_data: Datos extraídos del sitio web
        
    Returns:
        Diccionario con resultados de validación
    """
    validation_result = {
        'validacion_general': 'NO_VALIDADO',
        'nombre_coincide': 'NO_VERIFICADO',
        'promedio_coincide': 'NO_VERIFICADO',
        'folio_coincide': 'NO_VERIFICADO',
        'inconsistencias': '',
        'confiabilidad': 'BAJA'
    }
    
    try:
        inconsistencias = []
        coincidencias = 0
        validaciones_realizadas = 0
        
        def normalize_text(text: str) -> str:
            """Normaliza texto: reemplaza NBSP con espacio, elimina múltiples espacios y trim"""
            if not text:
                return ''
            text = text.replace('\u00A0', ' ')  # Reemplazar non-breaking space
            text = re.sub(r'\s+', ' ', text)  # Reemplazar múltiples espacios con uno
            return text.strip().upper()
        
        # VALIDACIÓN 1: NOMBRE (Crítico)
        qr_nombre = normalize_text(qr_data.get('nombre_alumno', ''))
        web_nombre = normalize_text(web_data.get('nombre', ''))
        
        if qr_nombre and web_nombre:
            validaciones_realizadas += 1
            if qr_nombre == web_nombre:
                validation_result['nombre_coincide'] = 'EXACTO'
                coincidencias += 1
            elif qr_nombre in web_nombre or web_nombre in qr_nombre:
                validation_result['nombre_coincide'] = 'PARCIAL'
                coincidencias += 0.7
            else:
                validation_result['nombre_coincide'] = 'NO_COINCIDE'
                inconsistencias.append(f"NOMBRE: QR='{qr_data.get('nombre_alumno', '')}' vs WEB='{web_data.get('nombre', '')}'")
        
        # VALIDACIÓN 2: PROMEDIO (Crítico) con manejo mejorado de formatos
        qr_promedio = qr_data.get('promedio', '').strip()
        web_promedio = web_data.get('promedio', '').strip()
        
        if qr_promedio and web_promedio:
            validaciones_realizadas += 1
            try:
                # Manejar formatos como "8.5/10"
                qr_prom_clean = re.sub(r'/.*', '', qr_promedio)
                web_prom_clean = re.sub(r'/.*', '', web_promedio)
                
                qr_prom_float = float(qr_prom_clean)
                web_prom_float = float(web_prom_clean)
                
                if abs(qr_prom_float - web_prom_float) < 0.01:
                    validation_result['promedio_coincide'] = 'EXACTO'
                    coincidencias += 1
                else:
                    validation_result['promedio_coincide'] = 'NO_COINCIDE'
                    inconsistencias.append(f"PROMEDIO: QR='{qr_promedio}' vs WEB='{web_promedio}'")
            except ValueError:
                validation_result['promedio_coincide'] = 'ERROR_FORMATO'
                inconsistencias.append(f"PROMEDIO: Error en formato - QR='{qr_promedio}' WEB='{web_promedio}'")
        
        # VALIDACIÓN 3: FOLIO (Informativo)
        qr_folio = qr_data.get('folio', '').strip()
        web_folio = web_data.get('folio', '').strip()
        
        if qr_folio and web_folio:
            validaciones_realizadas += 1
            if qr_folio == web_folio:
                validation_result['folio_coincide'] = 'EXACTO'
                coincidencias += 1
            else:
                validation_result['folio_coincide'] = 'NO_COINCIDE'
                inconsistencias.append(f"FOLIO: QR='{qr_folio}' vs WEB='{web_folio}'")
        
        # DETERMINACIÓN FINAL DE VALIDEZ
        if validaciones_realizadas == 0:
            validation_result['validacion_general'] = 'SIN_DATOS_SUFICIENTES'
            validation_result['confiabilidad'] = 'NO_DETERMINADA'
        else:
            porcentaje_coincidencia = (coincidencias / validaciones_realizadas) * 100
            
            if porcentaje_coincidencia >= 95:
                validation_result['validacion_general'] = 'VALIDO'
                validation_result['confiabilidad'] = 'ALTA'
            elif porcentaje_coincidencia >= 80:
                validation_result['validacion_general'] = 'PARCIALMENTE_VALIDO'
                validation_result['confiabilidad'] = 'MEDIA'
            else:
                validation_result['validacion_general'] = 'POSIBLE_FALSIFICACION'
                validation_result['confiabilidad'] = 'BAJA'
        
        validation_result['inconsistencias'] = '; '.join(inconsistencias)
        
    except Exception as e:
        logger.error(f"Error en validación: {e}")
        validation_result['inconsistencias'] = f"Error en validación: {str(e)}"
        validation_result['validacion_general'] = 'ERROR_VALIDACION'
    
    return validation_result
