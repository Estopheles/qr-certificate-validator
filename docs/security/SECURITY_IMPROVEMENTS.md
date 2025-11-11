# 🔒 Guía de Mejoras de Seguridad - QR Certificate Validator

## 🚨 Vulnerabilidades Críticas Identificadas

### 1. **Path Traversal (CWE-22/23) - CRÍTICO**

**Archivos Afectados:**
- `core/pdf_processor.py` (líneas 36-68, 80-81)
- `output/report_generator.py` (líneas 12-236)
- `utils/logger.py` (líneas 22-23)

**Problema:**
```python
# VULNERABLE - Permite acceso a archivos fuera del directorio permitido
pdf_path = os.path.join(folder_path, pdf_file)  # Sin validación
with open(self.log_file, 'w', encoding='utf-8') as f:  # Path no validado
```

**Solución:**
```python
import os
from pathlib import Path

def validate_safe_path(file_path: str, base_dir: str) -> bool:
    """Valida que el path esté dentro del directorio base permitido"""
    try:
        base_path = Path(base_dir).resolve()
        target_path = Path(file_path).resolve()
        return target_path.is_relative_to(base_path)
    except (OSError, ValueError):
        return False

def safe_join_path(base_dir: str, filename: str) -> str:
    """Une paths de forma segura"""
    # Sanitizar nombre de archivo
    safe_filename = os.path.basename(filename)
    if not safe_filename or safe_filename in ('.', '..'):
        raise ValueError("Nombre de archivo inválido")
    
    full_path = os.path.join(base_dir, safe_filename)
    
    if not validate_safe_path(full_path, base_dir):
        raise ValueError("Path fuera del directorio permitido")
    
    return full_path
```

### 2. **Server-Side Request Forgery (SSRF) - ALTO**

**Archivo Afectado:**
- `core/web_scraper.py` (líneas 125-137)

**Problema:**
```python
# VULNERABLE - Permite requests a cualquier URL
self.driver.get(url)  # Sin validación de dominio
```

**Solución:**
```python
import urllib.parse
from typing import Set

ALLOWED_DOMAINS: Set[str] = {
    'siged.sep.gob.mx',
    'www.siged.sep.gob.mx'
}

def validate_url(url: str) -> bool:
    """Valida que la URL sea segura y esté en dominios permitidos"""
    try:
        parsed = urllib.parse.urlparse(url)
        
        # Verificar esquema
        if parsed.scheme not in ('http', 'https'):
            return False
        
        # Verificar dominio permitido
        domain = parsed.netloc.lower()
        if domain not in ALLOWED_DOMAINS:
            return False
        
        # Verificar que no sea IP privada
        if _is_private_ip(domain):
            return False
            
        return True
    except Exception:
        return False

def _is_private_ip(hostname: str) -> bool:
    """Verifica si es una IP privada"""
    import ipaddress
    try:
        ip = ipaddress.ip_address(hostname)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return False  # No es IP, es hostname
```

### 3. **Manejo Inadecuado de Excepciones - ALTO**

**Archivos Afectados:**
- `main.py` (líneas 70-71, 75-76)
- `core/qr_detector.py` (líneas 49-50)
- `utils/logger.py` (líneas 38-39)

**Problema:**
```python
# VULNERABLE - Captura todas las excepciones sin especificar
except Exception as e:
    pass  # Silencia errores críticos
```

**Solución:**
```python
# Manejo específico de excepciones
try:
    results = process_single_pdf_with_validation(pdf_file, folder_path, process_log)
    all_results.extend(results)
except FileNotFoundError as e:
    logger.error(f"Archivo no encontrado {pdf_file}: {e}")
    process_log.log(f"ERROR_FILE_NOT_FOUND: {pdf_file}")
except PermissionError as e:
    logger.error(f"Sin permisos para {pdf_file}: {e}")
    process_log.log(f"ERROR_PERMISSION: {pdf_file}")
except ValueError as e:
    logger.error(f"Valor inválido en {pdf_file}: {e}")
    process_log.log(f"ERROR_VALUE: {pdf_file}")
except Exception as e:
    logger.error(f"Error inesperado procesando {pdf_file}: {e}")
    process_log.log(f"ERROR_UNEXPECTED: {pdf_file} - {type(e).__name__}")
    # Re-raise solo si es crítico
    if isinstance(e, (MemoryError, KeyboardInterrupt)):
        raise
```

### 4. **Vulnerabilidades en Dependencias - MEDIO**

**Archivo Afectado:**
- `requirements.txt` (líneas 20-21, 26-27)

**Problema:**
```
# Versiones con vulnerabilidades conocidas
lxml>=5.0.0  # Vulnerable a XXE
urllib3==1.26.18  # Vulnerabilidades de seguridad
```

**Solución:**
```
# requirements.txt actualizado
lxml>=4.9.3,<5.0.0  # Versión segura
urllib3>=2.0.0      # Versión actualizada
selenium>=4.17.0    # Última versión estable
pillow>=10.2.0      # Versión con parches de seguridad
```

## 🛡️ Implementaciones de Seguridad Requeridas

### 1. **Módulo de Validación de Seguridad**

**Crear:** `utils/security_validator.py`

```python
"""
Módulo de validación de seguridad
"""
import os
import re
import ipaddress
import urllib.parse
from pathlib import Path
from typing import Set, Optional
import logging

logger = logging.getLogger(__name__)

class SecurityValidator:
    """Validador de seguridad centralizado"""
    
    ALLOWED_DOMAINS: Set[str] = {
        'siged.sep.gob.mx',
        'www.siged.sep.gob.mx'
    }
    
    ALLOWED_FILE_EXTENSIONS: Set[str] = {
        '.pdf', '.xlsx', '.csv', '.json', '.txt', '.log'
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
    def validate_url(url: str) -> bool:
        """Valida que la URL sea segura"""
        try:
            parsed = urllib.parse.urlparse(url)
            
            # Verificar esquema
            if parsed.scheme not in ('http', 'https'):
                return False
            
            # Verificar dominio
            domain = parsed.netloc.lower()
            if domain not in SecurityValidator.ALLOWED_DOMAINS:
                logger.warning(f"Dominio no permitido: {domain}")
                return False
            
            # Verificar que no sea IP privada
            if SecurityValidator._is_private_ip(domain):
                logger.warning(f"IP privada detectada: {domain}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error validando URL {url}: {e}")
            return False
    
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
        """Sanitiza nombre de archivo"""
        # Remover caracteres peligrosos
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        safe_name = safe_name.strip('. ')
        
        # Verificar que no sea nombre reservado
        reserved_names = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 
                         'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 
                         'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 
                         'LPT7', 'LPT8', 'LPT9'}
        
        if safe_name.upper() in reserved_names:
            safe_name = f"file_{safe_name}"
        
        return safe_name[:255]  # Limitar longitud
```

### 2. **Actualizar main.py con Validaciones**

```python
# Agregar al inicio de main.py
from utils.security_validator import SecurityValidator

def validate_paths(input_folder: str, output_file: str) -> bool:
    """Valida que los paths sean válidos y seguros"""
    # Validar input folder
    if not os.path.exists(input_folder):
        print(f"Error: La carpeta de entrada {input_folder} no existe.")
        return False
    
    # Validar que input_folder esté en ubicación segura
    if not SecurityValidator.validate_file_path(input_folder, os.getcwd()):
        print(f"Error: Carpeta de entrada en ubicación no segura.")
        return False
    
    # Validar output file
    if not SecurityValidator.validate_file_path(output_file, os.getcwd()):
        print(f"Error: Archivo de salida en ubicación no segura.")
        return False
    
    # Resto de validaciones...
```

### 3. **Actualizar web_scraper.py**

```python
# En SeleniumSigedScraper.scrape_certificate()
def scrape_certificate(self, url: str) -> Dict:
    """Realiza scraping seguro del certificado"""
    
    # VALIDACIÓN DE SEGURIDAD
    if not SecurityValidator.validate_url(url):
        return {
            'success': False, 
            'error': 'URL no permitida o insegura', 
            'url': url
        }
    
    # Resto del código...
```

### 4. **Actualizar logger.py**

```python
# En ProcessLogger.__init__()
def __init__(self, log_file: Optional[str] = None):
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/process_log_{timestamp}.txt"
    
    # VALIDACIÓN DE SEGURIDAD
    if not SecurityValidator.validate_file_path(log_file, os.getcwd()):
        raise ValueError(f"Archivo de log en ubicación no segura: {log_file}")
    
    self.log_file = log_file
    # Resto del código...
```

## 🔧 Mejoras de Calidad de Código

### 1. **Logging Estructurado**

**Crear:** `utils/structured_logger.py`

```python
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
```

### 2. **Manejo de Configuración Segura**

**Actualizar:** `config.py`

```python
"""
Configuración segura del proyecto
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

def get_env_var(key: str, default: str = None, required: bool = False) -> str:
    """Obtiene variable de entorno con validación"""
    value = os.getenv(key, default)
    
    if required and not value:
        raise ValueError(f"Variable de entorno requerida no encontrada: {key}")
    
    return value

def validate_directory(path: str, create_if_missing: bool = False) -> str:
    """Valida y opcionalmente crea directorio"""
    path_obj = Path(path)
    
    if not path_obj.exists() and create_if_missing:
        try:
            path_obj.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directorio creado: {path}")
        except OSError as e:
            raise ValueError(f"No se pudo crear directorio {path}: {e}")
    
    if not path_obj.exists():
        raise ValueError(f"Directorio no existe: {path}")
    
    if not path_obj.is_dir():
        raise ValueError(f"Path no es directorio: {path}")
    
    return str(path_obj.absolute())

# Configuración con validación
try:
    DEFAULT_INPUT_PATH = validate_directory(
        get_env_var('DEFAULT_INPUT_PATH', '/home/christhianrodriguez/Documents/PDFs'),
        create_if_missing=True
    )
    DEFAULT_OUTPUT_PATH = validate_directory(
        get_env_var('DEFAULT_OUTPUT_PATH', '/home/christhianrodriguez/Documents/Resultados'),
        create_if_missing=True
    )
except ValueError as e:
    logger.error(f"Error en configuración: {e}")
    raise

# Timeouts con validación
SELENIUM_TIMEOUT_SHORT = max(1, int(get_env_var('SELENIUM_TIMEOUT_SHORT', '8')))
SELENIUM_TIMEOUT_MEDIUM = max(SELENIUM_TIMEOUT_SHORT, int(get_env_var('SELENIUM_TIMEOUT_MEDIUM', '14')))
SELENIUM_TIMEOUT_LONG = max(SELENIUM_TIMEOUT_MEDIUM, int(get_env_var('SELENIUM_TIMEOUT_LONG', '18')))
```

## 📋 Plan de Implementación

### **Fase 1: Seguridad Crítica (Prioridad Alta)**
- [ ] Implementar `SecurityValidator`
- [ ] Actualizar validación de paths en todos los módulos
- [ ] Agregar validación de URLs en web_scraper
- [ ] Actualizar requirements.txt con versiones seguras

### **Fase 2: Manejo de Errores (Prioridad Alta)**
- [ ] Reemplazar `except Exception` genéricas
- [ ] Implementar logging estructurado
- [ ] Agregar validación de entrada robusta
- [ ] Crear tests para casos de error

### **Fase 3: Mejoras de Calidad (Prioridad Media)**
- [ ] Refactorizar funciones largas
- [ ] Agregar type hints completos
- [ ] Implementar métricas de rendimiento
- [ ] Documentar APIs completamente

### **Fase 4: Monitoreo y Observabilidad (Prioridad Baja)**
- [ ] Agregar métricas de Prometheus
- [ ] Implementar health checks
- [ ] Crear dashboard de monitoreo
- [ ] Configurar alertas automáticas

## 🧪 Tests de Seguridad Requeridos

**Crear:** `tests/test_security.py`

```python
"""
Tests de seguridad
"""
import pytest
import tempfile
import os
from utils.security_validator import SecurityValidator

class TestSecurityValidator:
    
    def test_path_traversal_prevention(self):
        """Test prevención de path traversal"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Casos maliciosos
            malicious_paths = [
                "../../../etc/passwd",
                "..\\..\\windows\\system32",
                "/etc/passwd",
                "C:\\Windows\\System32"
            ]
            
            for path in malicious_paths:
                assert not SecurityValidator.validate_file_path(path, temp_dir)
    
    def test_url_validation(self):
        """Test validación de URLs"""
        # URLs válidas
        valid_urls = [
            "https://siged.sep.gob.mx/certificado/123",
            "http://www.siged.sep.gob.mx/cert/456"
        ]
        
        for url in valid_urls:
            assert SecurityValidator.validate_url(url)
        
        # URLs maliciosas
        malicious_urls = [
            "http://localhost:8080/admin",
            "https://192.168.1.1/config",
            "ftp://malicious.com/data",
            "javascript:alert('xss')"
        ]
        
        for url in malicious_urls:
            assert not SecurityValidator.validate_url(url)
```

## 📊 Métricas de Seguridad

**Implementar monitoreo de:**
- Intentos de path traversal
- URLs bloqueadas por validación
- Errores de autenticación/autorización
- Tiempo de respuesta de validaciones
- Uso de memoria y CPU durante procesamiento

## 🎯 Resultado Esperado

Después de implementar estas mejoras:

✅ **Eliminación de vulnerabilidades críticas**  
✅ **Código más robusto y mantenible**  
✅ **Mejor observabilidad y debugging**  
✅ **Cumplimiento de estándares de seguridad**  
✅ **Base sólida para escalabilidad futura**

**Tiempo estimado de implementación:** 2-3 semanas  
**Impacto en rendimiento:** Mínimo (<5% overhead)  
**Beneficio de seguridad:** Crítico (elimina vulnerabilidades mayores)