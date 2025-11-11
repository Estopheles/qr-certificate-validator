"""
Procesador de archivos PDF para extracción de códigos QR

Extrae una página del PDF como array numpy en memoria
    
    Args:
        pdf_path: Ruta al archivo PDF
        page_num: Número de página (default: 0)
        zoom: Factor de zoom
        dpi: DPI para la extracción
        
    Returns:
        Tupla con (imagen como array numpy, número de página, parámetro usado)
"""
import os
import time
import fitz  # PyMuPDF
import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging

from config import ZOOM_LEVELS, DPI_LEVELS
from core.qr_detector import advanced_qr_detection_memory, enhanced_parse_qr_data
from core.web_scraper import SeleniumSigedScraper
from core.validator import validate_certificate_data
from utils.logger import ProcessLogger
from utils.security_validator import SecurityValidator
from utils.structured_logger import StructuredLogger
from utils.pdf_security_analyzer import PDFSecurityAnalyzer

logger = logging.getLogger(__name__)
structured_logger = StructuredLogger(__name__)


def extract_page_as_image_memory(pdf_path: str, page_num: int = 0, 
                                zoom: Optional[float] = None, 
                                dpi: Optional[int] = None) -> Tuple[Optional[np.ndarray], int, float]:
    try:
        doc = fitz.open(pdf_path)
        if len(doc) == 0:
            return None, page_num, 0
        
        # Verificar si el PDF está encriptado
        if doc.is_encrypted:
            doc.close()
            return None, page_num, 0
        
        page = doc.load_page(page_num)
        param_value = zoom if zoom is not None else (dpi / 72.0 if dpi is not None else 2.0)
        mat = fitz.Matrix(param_value, param_value)
        pix = page.get_pixmap(matrix=mat, alpha=False)  # type: ignore
        
        # Procesar en memoria en lugar de guardar archivo
        img_data = pix.tobytes("png")
        doc.close()
        
        # Convertir a array numpy para OpenCV
        img_array = np.frombuffer(img_data, np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if image is not None:
            return image, page_num, param_value
        return None, page_num, param_value
    
    except Exception as e:
        logger.error(f"Error al procesar {pdf_path}: {e}")
        param_value = zoom if zoom is not None else (dpi / 72.0 if dpi is not None else 0)
        return None, page_num, param_value


def process_single_pdf_with_validation(pdf_file: str, folder_path: str, 
                                     process_log: ProcessLogger) -> List[Dict]:
    # VALIDACIÓN DE SEGURIDAD DE PATH
    try:
        pdf_path = SecurityValidator.safe_join_path(folder_path, pdf_file)
    except ValueError as e:
        logger.error(f"Path inseguro para {pdf_file}: {e}")
        structured_logger.log_security_event("SECURITY_ERROR", {"error": str(e)})
        return []
    
    # ANÁLISIS DE SEGURIDAD DEL PDF
    security_analyzer = PDFSecurityAnalyzer()
    security_analysis = security_analyzer.analyze_pdf_security(pdf_path)
    
    # Verificar si el PDF es seguro
    if security_analyzer.should_quarantine(security_analysis):
        risk_level = security_analysis.get('risk_assessment', {}).get('overall_risk', 'UNKNOWN')
        threats = security_analysis.get('risk_assessment', {}).get('threats', [])
        
        logger.warning(f"PDF {pdf_file} marcado como riesgoso: {risk_level}")
        process_log.log(f"SEGURIDAD: {pdf_file} - Riesgo {risk_level} - Amenazas: {len(threats)}")
        
        # Retornar resultado con información de seguridad
        return [{
            "archivo_pdf": pdf_file,
            "security_status": "QUARANTINE",
            "security_risk": risk_level,
            "security_threats": "; ".join(threats[:3]),  # Primeras 3 amenazas
            "security_recommendation": security_analysis.get('risk_assessment', {}).get('recommendation', ''),
            "qr_processing": "SKIPPED_SECURITY",
            "validacion_general": "BLOCKED_SECURITY"
        }]
    
    # Log de PDF seguro
    process_log.log(f"SEGURIDAD: {pdf_file} - SEGURO para procesamiento")
    
    results = []
    
    print(f"Procesando {pdf_file}...")
    process_log.log(f"PDF INICIO: {pdf_file}")
    start_time = time.time()
    
    try:
        # Configuraciones en orden de menor a mayor calidad
        configurations = []
        
        # Agregar configuraciones de zoom
        for zoom in ZOOM_LEVELS:
            configurations.append({'zoom': zoom, 'dpi': None})
        
        # Agregar configuraciones de DPI
        for dpi in DPI_LEVELS:
            configurations.append({'zoom': None, 'dpi': dpi})
        
        qr_codes_found = set()
        
        # Procesamiento optimizado: parar al encontrar QR
        for config in configurations:
            zoom = config['zoom']
            dpi = config['dpi']
            param_type = 'zoom' if zoom else 'dpi'
            param_value = zoom if zoom else dpi
            
            process_log.log(f"QR DETECCION: {pdf_file} - Probando {param_type}={param_value}")
            
            # Procesar imagen en memoria
            image_data = extract_page_as_image_memory(pdf_path, page_num=0, zoom=zoom, dpi=dpi)
            image, page_number, used_param = image_data
            
            if image is not None:
                try:
                    qr_data_list = advanced_qr_detection_memory(image)
                    
                    if qr_data_list:
                        process_log.log(f"QR DETECTADO: {pdf_file} - Con {param_type}={param_value}")
                        print(f"QR detectado con {param_type}={param_value}")
                        
                        for qr_data in qr_data_list:
                            if qr_data and qr_data not in qr_codes_found:
                                qr_codes_found.add(qr_data)
                                row = enhanced_parse_qr_data(qr_data)
                                
                                # DEBUG: Mostrar datos parseados del QR
                                print(f"\n=== 📋 ANÁLISIS QR ===")
                                print(f"📁 Archivo: {pdf_file}")
                                print(f"📄 Raw QR data: {repr(qr_data[:300])}...")
                                print(f"🔍 Datos parseados:")
                                print(f"  👤 Nombre: '{row.get('nombre_alumno', '')}'")
                                print(f"  🆔 CURP: '{row.get('curp', '')}'")
                                print(f"  📊 Promedio: '{row.get('promedio', '')}'")
                                print(f"  📅 Año: '{row.get('año', '')}'")
                                print(f"  🏛️  Autoridad: '{row.get('autoridad', '')}'")
                                print(f"  🔗 URL: '{row.get('url', '')}'")
                                print(f"  📋 Folio: '{row.get('folio', '')}'")
                                print(f"========================\n")
                                

                                
                                # Validación web si hay URL
                                web_data = {}
                                validation_data = {}
                                
                                if row.get('url'):
                                    print(f"Validando certificado en: {row['url']}")
                                    process_log.log(f"VALIDACION INICIO: {pdf_file} - URL: {row['url']}")
                                    
                                    scraper = SeleniumSigedScraper(headless=True, timeouts=[8, 14, 18])
                                    scrape_result = scraper.scrape_certificate(row['url'])
                                    
                                    if scrape_result.get('success'):
                                        web_data = scrape_result['certificate_info']
                                        
                                        # DEBUG: Mostrar datos del web
                                        print(f"🌐 === DATOS WEB EXTRAÍDOS ===")
                                        print(f"  👤 Nombre: '{web_data.get('nombre', '')}'")
                                        print(f"  📊 Promedio: '{web_data.get('promedio', '')}'")
                                        print(f"  📋 Folio: '{web_data.get('folio', '')}'")
                                        print(f"  📄 Tipo Doc: '{web_data.get('tipo_documento', '')}'")
                                        print(f"  🏛️  Autoridad: '{web_data.get('autoridad_emisora', '')}'")
                                        print(f"  🎓 Carrera: '{web_data.get('carrera', '')}'")
                                        print(f"==============================\n")
                                        

                                        
                                        validation_data = validate_certificate_data(row, web_data)
                                        print(f"Resultado validación: {validation_data['validacion_general']}")
                                        process_log.log(f"VALIDACION: {pdf_file} - {validation_data['validacion_general']}")
                                    else:
                                        print(f"Error al validar: {scrape_result.get('error', 'Desconocido')}")
                                        process_log.log(f"VALIDACION ERROR: {pdf_file} - {scrape_result.get('error', 'Desconocido')}")
                                        validation_data = {
                                            'validacion_general': 'ERROR_SCRAPING',
                                            'nombre_coincide': 'NO_VERIFICADO',
                                            'promedio_coincide': 'NO_VERIFICADO',
                                            'folio_coincide': 'NO_VERIFICADO',
                                            'inconsistencias': f"Error al acceder a URL: {scrape_result.get('error', 'Desconocido')}",
                                            'confiabilidad': 'NO_DETERMINADA'
                                        }
                                else:
                                    print("Sin URL para validación")
                                    process_log.log(f"VALIDACION: {pdf_file} - Sin URL")
                                    validation_data = {
                                        'validacion_general': 'SIN_URL',
                                        'nombre_coincide': 'NO_VERIFICADO',
                                        'promedio_coincide': 'NO_VERIFICADO',
                                        'folio_coincide': 'NO_VERIFICADO',
                                        'inconsistencias': 'No se encontró URL para validación',
                                        'confiabilidad': 'NO_DETERMINADA'
                                    }
                                
                                # Si el folio no está en QR pero sí en web, tomarlo de web
                                if not row.get('folio') and web_data.get('folio'):
                                    row['folio'] = web_data['folio']
                                
                                # Agregar datos del sitio web, validación y seguridad
                                additional_data = {
                                    "archivo_pdf": pdf_file,
                                    "pagina": page_number,
                                    "parametro_extraccion": used_param,
                                    "metodo": f"optimizado_memoria_{param_type}_{param_value}",
                                    # Datos de seguridad
                                    "security_status": "SAFE",
                                    "security_risk": security_analysis.get('risk_assessment', {}).get('overall_risk', 'SAFE'),
                                    "security_threats": "",
                                    "security_recommendation": security_analysis.get('risk_assessment', {}).get('recommendation', 'SEGURO'),
                                    # Datos del sitio web
                                    "web_nombre": web_data.get('nombre', ''),
                                    "web_promedio": web_data.get('promedio', ''),
                                    "web_folio": web_data.get('folio', ''),
                                    "web_tipo_documento": web_data.get('tipo_documento', ''),
                                    "web_autoridad_emisora": web_data.get('autoridad_emisora', ''),
                                    "web_carrera": web_data.get('carrera', ''),
                                    "web_fecha_registro": web_data.get('fecha_registro', ''),
                                    # Datos de validación
                                    "validacion_general": validation_data['validacion_general'],
                                    "nombre_coincide": validation_data['nombre_coincide'],
                                    "promedio_coincide": validation_data['promedio_coincide'],
                                    "folio_coincide": validation_data['folio_coincide'],
                                    "inconsistencias": validation_data['inconsistencias'],
                                    "confiabilidad": validation_data['confiabilidad']
                                }
                                row = {**row, **additional_data}
                                
                                results.append(row)
                        
                        # OPTIMIZACIÓN CLAVE: Salir inmediatamente tras encontrar QR
                        break
                        
                except Exception as e:
                    process_log.log(f"ERROR QR: {pdf_file} - {param_type}={param_value} - {str(e)}")
                    logger.error(f"Error al procesar imagen en memoria: {e}")
            else:
                process_log.log(f"ERROR IMAGEN: {pdf_file} - No se pudo generar con {param_type}={param_value}")
        
        if not results:
            process_log.log(f"QR NO ENCONTRADO: {pdf_file} - Todas las configuraciones fallaron")
            print(f"No se encontraron códigos QR en {pdf_file}")
        else:
            process_log.log(f"PDF COMPLETADO: {pdf_file} - {len(results)} QR procesados")
            
    except Exception as e:
        process_log.log(f"ERROR GENERAL: {pdf_file} - {str(e)}")
        logger.error(f"Error general al procesar {pdf_file}: {e}")
    
    processing_time = time.time() - start_time
    process_log.log(f"PDF TIEMPO: {pdf_file} - {processing_time:.2f} segundos")
    
    return results