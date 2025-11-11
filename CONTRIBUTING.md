# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al QR Certificate Validator! Esta guía te ayudará a participar en el desarrollo del proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Reportar Bugs](#reportar-bugs)
- [Solicitar Features](#solicitar-features)

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código:

- **Sé respetuoso** con otros contribuyentes
- **Sé constructivo** en tus comentarios y críticas
- **Sé paciente** con nuevos contribuyentes
- **Enfócate en el código**, no en las personas

## 🚀 Cómo Contribuir

### Tipos de Contribuciones Bienvenidas

- 🐛 **Corrección de bugs**
- ✨ **Nuevas características**
- 📚 **Mejoras en documentación**
- 🧪 **Pruebas adicionales**
- 🔧 **Optimizaciones de rendimiento**
- 🛡️ **Mejoras de seguridad**

### Proceso General

1. **Fork** el repositorio
2. **Crea una rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Realiza tus cambios** siguiendo los estándares
4. **Ejecuta las pruebas** (`pytest tests/ -v`)
5. **Commit** tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
6. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
7. **Abre un Pull Request**

## 🛠️ Configuración del Entorno

### Requisitos Previos

- Python 3.8+
- Git
- Chrome/Chromium (para web scraping)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/qr-certificate-validator.git
cd qr-certificate-validator

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Configurar pre-commit hooks
pre-commit install
```

### Verificar Instalación

```bash
# Ejecutar pruebas
pytest tests/ -v

# Verificar linting
flake8 .

# Verificar formateo
black --check .

# Verificar tipos
mypy .

# Verificar seguridad
python scripts/security_check.py
```

## 📝 Estándares de Código

### Estilo de Código

- **Formateo**: Usar `black` para formateo automático
- **Linting**: Seguir `flake8` para estilo
- **Tipos**: Usar type hints con `mypy`
- **Docstrings**: Formato Google/NumPy style

### Convenciones de Nomenclatura

```python
# Funciones: snake_case con nombres descriptivos en español
def process_single_pdf_with_validation():
    pass

# Variables: nombres descriptivos en español
pdf_files = []
qr_data_list = []

# Constantes: UPPER_CASE
SELENIUM_TIMEOUT_SHORT = 10

# Clases: PascalCase
class SecurityValidator:
    pass
```

### Estructura de Commits

```
tipo(alcance): descripción breve

Descripción más detallada si es necesaria.

- Cambio específico 1
- Cambio específico 2

Fixes #123
```

**Tipos de commit:**
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (no afectan funcionalidad)
- `refactor`: Refactorización de código
- `test`: Agregar o modificar pruebas
- `chore`: Tareas de mantenimiento

### Documentación

```python
def process_pdf_file(file_path: str, output_dir: str) -> List[Dict]:
    """
    Procesa un archivo PDF extrayendo códigos QR y validando certificados.
    
    Args:
        file_path: Ruta absoluta al archivo PDF
        output_dir: Directorio donde guardar resultados
        
    Returns:
        Lista de diccionarios con datos de certificados extraídos
        
    Raises:
        FileNotFoundError: Si el archivo PDF no existe
        ValueError: Si el archivo no es un PDF válido
        SecurityError: Si el PDF contiene contenido malicioso
        
    Example:
        >>> results = process_pdf_file("/path/to/cert.pdf", "/output")
        >>> len(results)
        3
    """
```

## 🔄 Proceso de Pull Request

### Antes de Enviar

- [ ] **Pruebas pasan**: `pytest tests/ -v`
- [ ] **Linting limpio**: `flake8 .`
- [ ] **Formateo correcto**: `black .`
- [ ] **Tipos válidos**: `mypy .`
- [ ] **Seguridad verificada**: `python scripts/security_check.py`
- [ ] **Documentación actualizada**

### Template de PR

```markdown
## 📝 Descripción
Breve descripción de los cambios realizados.

## 🔧 Tipo de Cambio
- [ ] Bug fix (cambio que corrige un problema)
- [ ] Nueva característica (cambio que agrega funcionalidad)
- [ ] Breaking change (cambio que rompe compatibilidad)
- [ ] Documentación

## 🧪 Pruebas
- [ ] Pruebas existentes pasan
- [ ] Nuevas pruebas agregadas
- [ ] Pruebas manuales realizadas

## 📋 Checklist
- [ ] Código sigue estándares del proyecto
- [ ] Auto-revisión realizada
- [ ] Documentación actualizada
- [ ] Sin warnings de linting
```

### Revisión de Código

Los PRs serán revisados considerando:

- **Funcionalidad**: ¿El código hace lo que debe hacer?
- **Seguridad**: ¿Introduce vulnerabilidades?
- **Rendimiento**: ¿Afecta negativamente el rendimiento?
- **Mantenibilidad**: ¿Es fácil de entender y mantener?
- **Pruebas**: ¿Está adecuadamente probado?

## 🐛 Reportar Bugs

### Antes de Reportar

1. **Busca** en issues existentes
2. **Verifica** que sea reproducible
3. **Prueba** con la última versión

### Template de Bug Report

```markdown
## 🐛 Descripción del Bug
Descripción clara y concisa del problema.

## 🔄 Pasos para Reproducir
1. Ir a '...'
2. Hacer clic en '...'
3. Ejecutar '...'
4. Ver error

## ✅ Comportamiento Esperado
Descripción de lo que debería pasar.

## 📱 Entorno
- OS: [e.g. Ubuntu 22.04]
- Python: [e.g. 3.9.7]
- Versión: [e.g. 1.2.3]

## 📎 Información Adicional
- Logs relevantes
- Screenshots si aplica
- Archivos de ejemplo (sin datos sensibles)
```

## ✨ Solicitar Features

### Template de Feature Request

```markdown
## 🚀 Descripción del Feature
Descripción clara de la funcionalidad deseada.

## 💡 Motivación
¿Por qué sería útil este feature?

## 📋 Solución Propuesta
Descripción de cómo podría implementarse.

## 🔄 Alternativas Consideradas
Otras formas de resolver el problema.

## 📎 Información Adicional
Contexto adicional, mockups, etc.
```

## 🧪 Escribir Pruebas

### Estructura de Pruebas

```python
import pytest
from unittest.mock import Mock, patch
from core.pdf_processor import process_single_pdf

class TestPDFProcessor:
    """Pruebas para el procesador de PDFs"""
    
    def test_process_valid_pdf(self):
        """Test procesamiento de PDF válido"""
        # Arrange
        pdf_path = "test_data/valid_certificate.pdf"
        
        # Act
        results = process_single_pdf(pdf_path)
        
        # Assert
        assert len(results) > 0
        assert results[0]['qr_data'] is not None
        
    def test_process_invalid_pdf_raises_error(self):
        """Test que PDF inválido lance error"""
        with pytest.raises(ValueError):
            process_single_pdf("invalid.pdf")
```

### Cobertura de Pruebas

```bash
# Ejecutar con cobertura
pytest --cov=. --cov-report=html tests/

# Ver reporte
open htmlcov/index.html
```

## 🔒 Consideraciones de Seguridad

### Reportar Vulnerabilidades

Para vulnerabilidades de seguridad, **NO** abras un issue público. En su lugar:

1. Envía email a: security@proyecto.com
2. Incluye descripción detallada
3. Proporciona pasos para reproducir
4. Sugiere posible solución si la tienes

### Revisión de Seguridad

Todo código que maneja:
- Archivos de usuario
- URLs externas
- Datos sensibles
- Operaciones del sistema

Debe pasar revisión de seguridad adicional.

## 📚 Recursos Adicionales

- [Documentación del Proyecto](docs/)
- [Guía de Arquitectura](docs/architecture.md)
- [API Reference](docs/api.md)
- [Troubleshooting](docs/troubleshooting/)

## 🙏 Reconocimientos

Todos los contribuyentes serán reconocidos en:
- README.md
- CONTRIBUTORS.md
- Releases notes

¡Gracias por contribuir al QR Certificate Validator! 🚀