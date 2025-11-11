# 🧪 Tests

Suite completa de pruebas para QR Certificate Validator.

## 📁 Estructura de Tests

```
tests/
├── unit/                   # Pruebas unitarias
│   ├── test_pdf_processor.py     # Tests del procesador PDF
│   ├── test_qr_detector.py       # Tests del detector QR
│   ├── test_security.py          # Tests de seguridad
│   └── test_validator.py         # Tests del validador
├── integration/            # Pruebas de integración
│   └── __init__.py
└── __init__.py
```

## 🚀 Ejecutar Tests

### Todos los Tests
```bash
# Ejecutar toda la suite
pytest tests/ -v

# Con coverage
pytest tests/ --cov=. --cov-report=html
```

### Tests Específicos
```bash
# Solo tests de seguridad
pytest tests/unit/test_security.py -v

# Solo tests de PDF processing
pytest tests/unit/test_pdf_processor.py -v

# Solo tests de QR detection
pytest tests/unit/test_qr_detector.py -v

# Solo tests de validación
pytest tests/unit/test_validator.py -v
```

### Tests con Filtros
```bash
# Tests que contengan "security" en el nombre
pytest tests/ -k "security" -v

# Tests marcados como "slow"
pytest tests/ -m "slow" -v

# Excluir tests lentos
pytest tests/ -m "not slow" -v
```

## 📋 Categorías de Tests

### 🔒 Tests de Seguridad (`test_security.py`)
- **Path traversal prevention**: Validación de rutas seguras
- **SSRF protection**: Prevención de ataques SSRF
- **PDF malware detection**: Detección de PDFs maliciosos
- **Input sanitization**: Sanitización de entradas

### 📄 Tests de PDF Processing (`test_pdf_processor.py`)
- **PDF parsing**: Lectura correcta de PDFs
- **QR extraction**: Extracción de códigos QR
- **Error handling**: Manejo de PDFs corruptos
- **Memory management**: Gestión eficiente de memoria

### 🔍 Tests de QR Detection (`test_qr_detector.py`)
- **Multi-algorithm detection**: Detección con múltiples algoritmos
- **Data parsing**: Parseo correcto de datos QR
- **Format validation**: Validación de formatos
- **Edge cases**: Casos límite y errores

### ✅ Tests de Validation (`test_validator.py`)
- **Web scraping**: Validación web correcta
- **Data comparison**: Comparación de datos QR vs web
- **Confidence scoring**: Cálculo de confiabilidad
- **Error recovery**: Recuperación de errores de red

## 🛠️ Configuración de Tests

### Dependencias de Testing
```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt
```

### Variables de Entorno para Tests
```bash
# Crear archivo .env.test
cp .env.example .env.test

# Configurar para testing
export TESTING=true
export LOG_LEVEL=DEBUG
export SELENIUM_TIMEOUT_SHORT=5
```

### Fixtures y Datos de Prueba
- **PDFs de prueba**: Ubicados en `tests/fixtures/`
- **Datos mock**: Respuestas simuladas para web scraping
- **Configuración temporal**: Archivos de configuración para tests

## 📊 Coverage y Métricas

### Objetivos de Coverage
- **Mínimo aceptable**: 80%
- **Objetivo**: 90%+
- **Crítico (seguridad)**: 95%+

### Generar Reporte de Coverage
```bash
# HTML report
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html

# Terminal report
pytest tests/ --cov=. --cov-report=term-missing

# XML report (para CI/CD)
pytest tests/ --cov=. --cov-report=xml
```

## 🔄 Integración Continua

### GitHub Actions
```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest tests/ --cov=. --cov-report=xml
```

### Pre-commit Hooks
```bash
# Instalar pre-commit
pip install pre-commit
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

## 🐛 Debugging Tests

### Tests Fallidos
```bash
# Ejecutar con más detalle
pytest tests/unit/test_security.py::test_path_traversal -vvv

# Parar en el primer fallo
pytest tests/ -x

# Entrar en debugger en fallos
pytest tests/ --pdb
```

### Logs Durante Tests
```bash
# Mostrar logs durante tests
pytest tests/ -s --log-cli-level=DEBUG

# Capturar solo logs de error
pytest tests/ --log-cli-level=ERROR
```

## ✅ Checklist para Nuevos Tests

Antes de agregar nuevos tests, asegúrate de:

- [ ] **Nombre descriptivo** del test
- [ ] **Docstring** explicando qué se prueba
- [ ] **Setup y teardown** apropiados
- [ ] **Assertions claras** y específicas
- [ ] **Casos edge** cubiertos
- [ ] **Mocks apropiados** para dependencias externas
- [ ] **Performance** considerada (tests rápidos)

## 📝 Escribir Nuevos Tests

### Ejemplo de Test Unitario
```python
def test_pdf_security_analysis():
    """Test que el análisis de seguridad detecta PDFs maliciosos"""
    # Arrange
    malicious_pdf = create_test_pdf_with_javascript()
    
    # Act
    result = analyze_pdf_security(malicious_pdf)
    
    # Assert
    assert result['status'] == 'MALICIOUS'
    assert 'javascript' in result['threats']
    assert result['risk_level'] == 'HIGH'
```

### Ejemplo de Test de Integración
```python
@pytest.mark.integration
def test_full_pdf_processing_pipeline():
    """Test del pipeline completo de procesamiento"""
    # Arrange
    test_pdf_path = "tests/fixtures/sample_certificate.pdf"
    
    # Act
    results = process_single_pdf_with_validation(test_pdf_path, ".", mock_logger)
    
    # Assert
    assert len(results) > 0
    assert results[0]['nombre_alumno'] != ''
    assert results[0]['validacion_general'] in ['VALIDO', 'PARCIALMENTE_VALIDO']
```

## 🎯 Mejores Prácticas

1. **Tests independientes**: Cada test debe poder ejecutarse solo
2. **Datos determinísticos**: Usar datos fijos, no aleatorios
3. **Mocks apropiados**: Mockear dependencias externas (web, filesystem)
4. **Tests rápidos**: Mantener tiempo de ejecución bajo
5. **Cleanup**: Limpiar recursos después de cada test
6. **Documentación**: Explicar qué y por qué se prueba