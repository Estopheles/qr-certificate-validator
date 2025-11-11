"""
Web scraper para validación de certificados SIGED
"""
import re
import logging
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup

from config import SELENIUM_TIMEOUT_SHORT, SELENIUM_TIMEOUT_MEDIUM, SELENIUM_TIMEOUT_LONG, SELENIUM_HEADLESS
from utils.progress_bar import show_progress_bar
from utils.security_validator import SecurityValidator
from utils.structured_logger import StructuredLogger

logger = logging.getLogger(__name__)
structured_logger = StructuredLogger(__name__)


class SeleniumSigedScraper:
    """Scraper para extraer datos de certificados del sitio SIGED"""
    
    def __init__(self, headless: bool = SELENIUM_HEADLESS, timeouts: List[int] = None):
        self.headless = headless
        self.timeouts = timeouts or [SELENIUM_TIMEOUT_SHORT, SELENIUM_TIMEOUT_MEDIUM, SELENIUM_TIMEOUT_LONG]
        self.driver = None
        
    def setup_driver(self) -> bool:
        """Configura el driver de Chrome con opciones optimizadas."""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            logger.error(f"Error iniciando driver: {e}")
            return False
    
    def extract_certificate_data(self) -> Dict[str, str]:
        """Extrae datos del certificado del HTML cargado"""
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        
        text = soup.get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        certificate_data = {}
        
        # Buscar datos usando patrones más robustos
        for line in lines:
            line_lower = line.lower().strip()
            
            # Nombre
            if 'nombre:' in line_lower and 'nombre' not in certificate_data:
                nombre_match = re.search(r'nombre:\s*(.+)', line, re.IGNORECASE)
                if nombre_match:
                    certificate_data['nombre'] = nombre_match.group(1).strip()
            
            # Promedio
            elif 'promedio:' in line_lower and 'promedio' not in certificate_data:
                promedio_match = re.search(r'promedio:\s*(\d+\.?\d*)', line, re.IGNORECASE)
                if promedio_match:
                    certificate_data['promedio'] = promedio_match.group(1)
            
            # Folio
            elif 'folio:' in line_lower and 'folio' not in certificate_data:
                folio_match = re.search(r'folio:\s*(.+)', line, re.IGNORECASE)
                if folio_match:
                    certificate_data['folio'] = folio_match.group(1).strip()
            
            # Autoridad emisora
            elif 'autoridad emisora:' in line_lower and 'autoridad_emisora' not in certificate_data:
                autoridad_match = re.search(r'autoridad emisora:\s*(.+)', line, re.IGNORECASE)
                if autoridad_match:
                    certificate_data['autoridad_emisora'] = autoridad_match.group(1).strip()
            
            # Tipo de documento
            elif 'tipo de documento:' in line_lower and 'tipo_documento' not in certificate_data:
                tipo_doc_match = re.search(r'tipo de documento:\s*(.+)', line, re.IGNORECASE)
                if tipo_doc_match:
                    certificate_data['tipo_documento'] = tipo_doc_match.group(1).strip()
            
            # Carrera
            elif 'carrera:' in line_lower and 'carrera' not in certificate_data:
                carrera_match = re.search(r'carrera:\s*(.+)', line, re.IGNORECASE)
                if carrera_match:
                    certificate_data['carrera'] = carrera_match.group(1).strip()
            
            # Fecha de registro
            elif 'fecha de registro en siged:' in line_lower and 'fecha_registro' not in certificate_data:
                fecha_match = re.search(r'fecha de registro en siged:\s*(.+)', line, re.IGNORECASE)
                if fecha_match:
                    certificate_data['fecha_registro'] = fecha_match.group(1).strip()
            
        # Búsqueda alternativa con Selenium
        self._extract_with_selenium_elements(certificate_data)
        
        return certificate_data
    
    def _extract_with_selenium_elements(self, certificate_data: Dict[str, str]):
        """Extrae datos usando selectores específicos de Selenium con búsqueda mejorada"""
        try:
            all_elements = self.driver.find_elements(By.XPATH, "//*[text()]")
            
            for element in all_elements:
                text = element.text.strip()
                if not text:
                    continue
                
                text_lower = text.lower()
                
                # Nombre
                if 'nombre:' in text_lower and 'nombre' not in certificate_data:
                    nombre_match = re.search(r'nombre:\s*(.+)', text, re.IGNORECASE)
                    if nombre_match:
                        certificate_data['nombre'] = nombre_match.group(1).strip()
                
                # Promedio
                elif 'promedio:' in text_lower and 'promedio' not in certificate_data:
                    promedio_match = re.search(r'promedio:\s*(\d+\.?\d*)', text, re.IGNORECASE)
                    if promedio_match:
                        certificate_data['promedio'] = promedio_match.group(1)
                
                # Folio
                elif 'folio:' in text_lower and 'folio' not in certificate_data:
                    folio_match = re.search(r'folio:\s*(.+)', text, re.IGNORECASE)
                    if folio_match:
                        certificate_data['folio'] = folio_match.group(1).strip()
                
                # Autoridad emisora
                elif 'autoridad emisora:' in text_lower and 'autoridad_emisora' not in certificate_data:
                    autoridad_match = re.search(r'autoridad emisora:\s*(.+)', text, re.IGNORECASE)
                    if autoridad_match:
                        certificate_data['autoridad_emisora'] = autoridad_match.group(1).strip()
                
                # Tipo de documento
                elif 'tipo de documento:' in text_lower and 'tipo_documento' not in certificate_data:
                    tipo_doc_match = re.search(r'tipo de documento:\s*(.+)', text, re.IGNORECASE)
                    if tipo_doc_match:
                        certificate_data['tipo_documento'] = tipo_doc_match.group(1).strip()
                
                # Carrera
                elif 'carrera:' in text_lower and 'carrera' not in certificate_data:
                    carrera_match = re.search(r'carrera:\s*(.+)', text, re.IGNORECASE)
                    if carrera_match:
                        certificate_data['carrera'] = carrera_match.group(1).strip()
                
                # Fecha de registro
                elif 'fecha de registro en siged:' in text_lower and 'fecha_registro' not in certificate_data:
                    fecha_match = re.search(r'fecha de registro en siged:\s*(.+)', text, re.IGNORECASE)
                    if fecha_match:
                        certificate_data['fecha_registro'] = fecha_match.group(1).strip()
        
        except Exception as e:
            logger.error(f"Error en extracción mejorada con selectores: {e}")
    
    def scrape_certificate(self, url: str) -> Dict:
        """Realiza scraping seguro del certificado con timeouts escalonados"""
        
        # VALIDACIÓN DE SEGURIDAD AVANZADA
        url_validation = SecurityValidator.validate_url(url)
        
        if not url_validation['valid']:
            classification = url_validation['classification']
            reason = url_validation['reason']
            
            # Log de seguridad según clasificación
            if classification == 'FRAUD':
                structured_logger.log_security_event("FRAUD_DETECTED", {
                    "url": url, 
                    "reason": reason,
                    "classification": classification
                })
                return {
                    'success': False, 
                    'error': f'🚨 POSIBLE FRAUDE: {reason}', 
                    'classification': 'FRAUD',
                    'url': url
                }
            elif classification == 'OTHER_STATE':
                structured_logger.log_security_event("OTHER_STATE_DOMAIN", {
                    "url": url, 
                    "reason": reason
                })
                return {
                    'success': False, 
                    'error': f'⚠️ REVISIÓN MANUAL: {reason}', 
                    'classification': 'OTHER_STATE',
                    'url': url
                }
            else:
                structured_logger.log_security_event("BLOCKED_URL", {
                    "url": url, 
                    "reason": reason,
                    "classification": classification
                })
                return {
                    'success': False, 
                    'error': f'🚫 URL BLOQUEADA: {reason}', 
                    'classification': classification,
                    'url': url
                }
        
        # Solo proceder si la URL es oficial y aprobada
        for attempt, timeout in enumerate(self.timeouts, 1):
            # Reiniciar driver en el primer intento
            if attempt == 1:
                if self.driver:
                    self.driver.quit()
                    self.driver = None
                
                if not self.setup_driver():
                    continue
            
            try:
                self.driver.get(url)
                
                # Mostrar progreso
                show_progress_bar(timeout, "Cargando certificado", attempt, len(self.timeouts))
                
                certificate_data = self.extract_certificate_data()
                
                if len(certificate_data) > 0:
                    return {
                        'success': True,
                        'method': f'selenium_timeout_{timeout}s_attempt_{attempt}',
                        'wait_time': timeout,
                        'certificate_info': certificate_data,
                        'url': url
                    }
                    
            except Exception as e:
                logger.error(f"Error durante el scraping de {url} en intento {attempt}: {e}")
        
        # Cerrar driver tras fallar todos los intentos
        if self.driver:
            self.driver.quit()
            self.driver = None
        
        return {
            'success': False,
            'error': f'Falló después de {len(self.timeouts)} intentos',
            'method': 'selenium_error',
            'url': url
        }
    
    def __del__(self):
        """Asegurar que el driver se cierre al destruir el objeto"""
        if self.driver:
            self.driver.quit()
