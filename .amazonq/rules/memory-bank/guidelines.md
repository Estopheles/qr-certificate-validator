# QR Certificate Validator - Development Guidelines

## Code Quality Standards

### Documentation Patterns
- **Module Docstrings**: All modules start with triple-quoted Spanish descriptions
- **Function Documentation**: Comprehensive docstrings with Args/Returns sections
- **Inline Comments**: Spanish comments explaining complex logic
- **Type Hints**: Extensive use of typing module (Dict, List, Optional, Tuple)

### Naming Conventions
- **Functions**: Snake_case with descriptive Spanish names (`process_single_pdf_with_validation`)
- **Variables**: Spanish descriptive names (`pdf_files`, `qr_data_list`, `certificate_data`)
- **Constants**: UPPER_CASE from config module (`SELENIUM_TIMEOUT_SHORT`, `ZOOM_LEVELS`)
- **Classes**: PascalCase with descriptive names (`SeleniumSigedScraper`, `SecurityValidator`)

### Import Organization
```python
# Standard library imports first
import os
import time
import logging
from typing import Dict, List, Optional

# Third-party imports
import cv2
import numpy as np
from selenium import webdriver

# Local imports last
from config import ZOOM_LEVELS
from utils.security_validator import SecurityValidator
```

## Security-First Development

### Input Validation Pattern
Every function handling external input follows this pattern:
```python
# VALIDACIÓN DE SEGURIDAD (always in Spanish comments)
try:
    validated_path = SecurityValidator.safe_join_path(base_path, user_input)
except ValueError as e:
    logger.error(f"Path inseguro para {file}: {e}")
    structured_logger.log_security_event("SECURITY_ERROR", {"error": str(e)})
    return []
```

### URL Validation Standard
```python
if not SecurityValidator.validate_url(url):
    structured_logger.log_security_event("BLOCKED_URL", {
        "url": url, 
        "reason": "URL no permitida o insegura"
    })
    return {'success': False, 'error': 'URL no permitida o insegura'}
```

### Security Logging Requirements
- All security events must be logged with `structured_logger.log_security_event()`
- Include context data in structured format
- Use Spanish error messages for user-facing errors

## Error Handling Architecture

### Exception Hierarchy
```python
try:
    # Main operation
    pass
except FileNotFoundError as e:
    logger.error(f"Archivo no encontrado {file}: {e}")
    structured_logger.log_processing_event(file, "FILE_NOT_FOUND", {"error": str(e)})
except PermissionError as e:
    logger.error(f"Sin permisos para {file}: {e}")
    structured_logger.log_processing_event(file, "PERMISSION_ERROR", {"error": str(e)})
except ValueError as e:
    logger.error(f"Valor inválido en {file}: {e}")
    structured_logger.log_processing_event(file, "VALUE_ERROR", {"error": str(e)})
except Exception as e:
    logger.error(f"Error inesperado procesando {file}: {e}")
    # Re-raise only critical errors
    if isinstance(e, (MemoryError, KeyboardInterrupt)):
        raise
```

### Graceful Degradation
- Continue processing other files when one fails
- Return empty lists/dicts instead of None for failed operations
- Log all errors but don't stop entire process

## Processing Patterns

### Memory-Efficient Processing
```python
# Process images in memory, not as temporary files
img_data = pix.tobytes("png")
img_array = np.frombuffer(img_data, np.uint8)
image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
```

### Optimization Strategy
- **Early Exit**: Stop processing when QR found (`break` after successful detection)
- **Configuration Loops**: Try multiple parameters (zoom, DPI) in order of efficiency
- **Resource Cleanup**: Always close resources (`doc.close()`, `driver.quit()`)

### Progress Tracking Pattern
```python
process_log.log(f"PDF INICIO: {pdf_file}")
# ... processing ...
process_log.log(f"PDF COMPLETADO: {pdf_file} - {len(results)} QR procesados")
processing_time = time.time() - start_time
process_log.log(f"PDF TIEMPO: {pdf_file} - {processing_time:.2f} segundos")
```

## Configuration Management

### Environment-Driven Configuration
- All configurable values in `config.py` with validation
- Environment variables with sensible defaults
- Path validation and auto-creation for directories

### Timeout Strategies
```python
# Escalating timeouts for web operations
self.timeouts = [SELENIUM_TIMEOUT_SHORT, SELENIUM_TIMEOUT_MEDIUM, SELENIUM_TIMEOUT_LONG]
for attempt, timeout in enumerate(self.timeouts, 1):
    # Try operation with current timeout
```

## Data Processing Standards

### Text Normalization
```python
def normalize_text(text: str) -> str:
    """Normaliza texto: reemplaza NBSP con espacio, elimina múltiples espacios"""
    if not text:
        return ''
    text = text.replace('\u00A0', ' ')  # Non-breaking space
    text = re.sub(r'\s+', ' ', text)    # Multiple spaces to single
    return text.strip().upper()
```

### Validation Logic
- Use percentage-based validation (95% = VALID, 80% = PARTIAL, <80% = INVALID)
- Accumulate inconsistencies in lists for detailed reporting
- Handle format variations (e.g., "8.5/10" promedio format)

## Testing Patterns

### Security Test Structure
```python
class TestSecurityValidator:
    def test_path_traversal_prevention(self):
        """Test prevención de path traversal"""
        malicious_paths = ["../../../etc/passwd", "..\\..\\windows\\system32"]
        for path in malicious_paths:
            assert not SecurityValidator.validate_file_path(path, base_dir)
```

### Test Data Management
- Use `tempfile.TemporaryDirectory()` for isolated test environments
- Create test files with `Path(file).touch()` for existence tests
- Test both positive and negative cases for all validators

## Logging Architecture

### Structured Logging Format
```python
# Processing events
structured_logger.log_processing_event(filename, "SUCCESS", {"qr_count": len(results)})

# Security events  
structured_logger.log_security_event("BLOCKED_URL", {"url": url, "reason": "Domain not allowed"})
```

### Log Categories
- **PDF INICIO/COMPLETADO**: File processing lifecycle
- **QR DETECCION/DETECTADO**: QR detection attempts and successes
- **VALIDACION**: Certificate validation results
- **SECURITY_ERROR**: Security violations and blocks

## Resource Management

### Driver Management
```python
def __del__(self):
    """Asegurar que el driver se cierre al destruir el objeto"""
    if self.driver:
        self.driver.quit()
```

### Cleanup Patterns
```python
def cleanup_all_temp_files():
    """Limpia todos los archivos temporales generados"""
    temp_files = glob.glob("temp_*.png")
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except Exception:
            pass  # Silent cleanup
```

## API Design Principles

### Return Value Consistency
- Functions return empty lists `[]` on failure, not None
- Web scraping returns structured dicts with `success` boolean
- Include metadata in returns (`method`, `wait_time`, `url`)

### Parameter Validation
- Validate all inputs at function entry
- Use type hints for all parameters
- Provide sensible defaults for optional parameters

### Function Composition
- Single responsibility per function
- Clear data flow between processing stages
- Minimal coupling between modules through well-defined interfaces