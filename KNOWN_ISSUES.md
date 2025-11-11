# 🐛 Issues Conocidos y Oportunidades de Mejora

Este documento lista los problemas identificados por análisis de código estático y oportunidades de mejora para contribuyentes.

## 🚨 Issues Críticos

### ✅ CWE-798 - Hardcoded Credentials (RESUELTO)
**Archivos afectados:** `core/qr_detector.py`
- **Estado:** ✅ **CORREGIDO** - Movido a configuración
- **Descripción:** Credenciales hardcodeadas movidas a variables de entorno
- **Commit:** Configuración externalizada en config.py

**Cómo contribuir:**
```bash
# Revisar estas líneas específicas
git checkout -b fix/hardcoded-credentials
# Examinar qr_detector.py líneas 161 y 183
# Mover cualquier credencial a variables de entorno
```

### 🔄 CWE-22 - Path Traversal (PARCIALMENTE RESUELTO)
**Archivos afectados:** `utils/security_validator.py`, `utils/logger.py`, `config.py`
- **Estado:** 🔄 **PARCIAL** - config.py corregido, otros pendientes
- **Descripción:** Vulnerabilidades de path traversal en múltiples archivos
- **Prioridad:** 🔴 Alta
- **Dificultad:** 🟡 Media
- **Progreso:** 1/3 archivos corregidos

**Cómo contribuir:**
```python
# Ejemplo de fix necesario
def safe_path_join(base_path, user_path):
    # Validar que user_path no contenga ../
    # Usar Path.resolve() para normalizar
    # Verificar que el resultado esté dentro de base_path
```

## ⚠️ Issues de Seguridad

### CWE-918 - Server-Side Request Forgery (SSRF)
**Archivos afectados:** `core/pdf_processor.py`, `core/web_scraper.py`
- **Líneas:** 151-179, 173-195
- **Descripción:** Posibles vulnerabilidades SSRF en requests web
- **Prioridad:** 🟠 Alta
- **Dificultad:** 🔴 Difícil

**Cómo contribuir:**
- Implementar whitelist de dominios más estricta
- Validar IPs antes de hacer requests
- Agregar timeouts más cortos
- Implementar rate limiting

### CWE-77/78/88 - OS Command Injection
**Archivos afectados:** `scripts/security_check.py`
- **Líneas:** 70-72
- **Descripción:** Posible inyección de comandos OS
- **Prioridad:** 🟠 Alta
- **Dificultad:** 🟡 Media

## 🔧 Issues de Mantenibilidad

### Readability and Maintainability Issues
**Archivos afectados:** Múltiples archivos
- **Descripción:** Código complejo, funciones largas, lógica difícil de seguir
- **Prioridad:** 🟡 Media
- **Dificultad:** 🟢 Fácil

**Archivos principales:**
- `utils/security_validator.py` (líneas 35-36, 94-95, 116-117)
- `core/web_scraper.py` (líneas 128-169, 180-182)
- `output/report_generator.py` (líneas 30-85)

**Cómo contribuir:**
- Dividir funciones grandes en funciones más pequeñas
- Agregar docstrings más descriptivos
- Simplificar lógica condicional compleja
- Extraer constantes mágicas

### High Cyclomatic Complexity
**Archivos afectados:** `core/qr_detector.py`, `core/web_scraper.py`
- **Líneas:** 75-76, 116-117, 55-56
- **Descripción:** Funciones con demasiadas decisiones/ramas
- **Prioridad:** 🟡 Media
- **Dificultad:** 🟡 Media

## 🚀 Issues de Rendimiento

### Performance Inefficiencies
**Archivos afectados:** Múltiples archivos
- **Descripción:** Operaciones ineficientes, loops innecesarios
- **Prioridad:** 🟡 Media
- **Dificultad:** 🟡 Media

**Archivos principales:**
- `utils/structured_logger.py` (línea 22-23)
- `core/web_scraper.py` (líneas 71-108, 119-120)
- `output/report_generator.py` (líneas 59-63, 240-241)

## 📝 Issues de Logging

### Insufficient or Improper Logging
**Archivos afectados:** Múltiples archivos
- **Descripción:** Logging insuficiente o inadecuado
- **Prioridad:** 🟢 Baja
- **Dificultad:** 🟢 Fácil

**Cómo contribuir:**
- Agregar más logs informativos
- Usar niveles de log apropiados
- Estructurar mejor los mensajes de log
- Agregar contexto a los logs de error

## 🧪 Issues de Testing

### Inadequate Error Handling
**Archivos afectados:** Múltiples archivos
- **Descripción:** Manejo de errores insuficiente o genérico
- **Prioridad:** 🟡 Media
- **Dificultad:** 🟡 Media

**Archivos principales:**
- `utils/cli_handler.py` (líneas 99-105)
- `core/validator.py` (líneas 57-58)
- `scripts/security_check.py` (líneas 56-58, 88-89)

## 🎯 Cómo Contribuir

### 1. Elegir un Issue
```bash
# Issues para principiantes (🟢 Fácil)
- Mejorar logging
- Agregar docstrings
- Refactorizar funciones pequeñas

# Issues intermedios (🟡 Media)
- Reducir complejidad ciclomática
- Mejorar manejo de errores
- Optimizar rendimiento

# Issues avanzados (🔴 Difícil)
- Vulnerabilidades de seguridad
- Arquitectura del sistema
- Integración de nuevas funcionalidades
```

### 2. Setup del Entorno
```bash
git clone https://github.com/tu-usuario/qr-certificate-validator.git
cd qr-certificate-validator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Crear Branch
```bash
git checkout -b fix/issue-description
# Ejemplo: git checkout -b fix/path-traversal-security
```

### 4. Ejecutar Tests y Análisis
```bash
# Antes de hacer cambios
pytest tests/ -v
python scripts/security_check.py

# Después de hacer cambios
pytest tests/ -v
flake8 .
black --check .
mypy .

# Análisis de seguridad completo
python security_scan.py .
```

### 5. Crear Pull Request
- Describir el problema solucionado
- Incluir tests si es aplicable
- Referenciar el issue: "Fixes #123"
- Seguir el template de PR

## 📊 Estadísticas de Issues (Actualizado 2025)

| Categoría | Críticos | Altos | Medios | Bajos | Total | Resueltos |
|-----------|----------|-------|--------|-------|-------|----------|
| Seguridad | 1 | 35 | 45 | 8 | 89 | 2 |
| Mantenibilidad | 0 | 5 | 25 | 15 | 45 | 0 |
| Rendimiento | 0 | 8 | 12 | 5 | 25 | 0 |
| Logging | 0 | 2 | 8 | 3 | 13 | 0 |
| Manejo de Errores | 0 | 15 | 20 | 5 | 40 | 2 |
| **Total** | **1** | **65** | **110** | **36** | **212** | **4** |

### 🏆 Progreso de Corrección: 4/212 (1.9%)

## 🏆 Contribuyentes Buscados

### 🔒 Security Experts
- Experiencia con OWASP Top 10
- Conocimiento de vulnerabilidades web
- Experiencia con análisis estático de código

### 🏗️ Software Architects
- Refactoring de código legacy
- Patrones de diseño
- Optimización de rendimiento

### 🧪 QA Engineers
- Escritura de tests unitarios
- Testing de seguridad
- Automatización de pruebas

### 📚 Technical Writers
- Documentación de código
- Guías de usuario
- Tutoriales y ejemplos

## 📞 Contacto

- **Issues**: Crear issue en GitHub
- **Discussions**: GitHub Discussions
- **Email**: christhian.rodriguez@example.com

## 🙏 Reconocimientos

Todos los contribuyentes serán reconocidos en:
- README.md
- CONTRIBUTORS.md
- Release notes

¡Gracias por ayudar a mejorar QR Certificate Validator! 🚀