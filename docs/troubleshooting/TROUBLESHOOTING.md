# 🔧 Guía de Solución de Problemas

## 🚨 Problemas Comunes y Soluciones

### 1. **Error de Compilación de lxml**

**Problema:**
```
ERROR: Failed building wheel for lxml
Failed to build lxml
```

**Soluciones:**

#### **Opción A: Script Automático (Recomendado)**
```bash
./install_dependencies.sh
```

#### **Opción B: Manual por Sistema Operativo**

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install -y python3-devel libxml2-devel libxslt-devel gcc gcc-c++
pip install --only-binary=lxml lxml
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3-dev libxml2-dev libxslt-dev build-essential
pip install --only-binary=lxml lxml
```

**macOS:**
```bash
brew install libxml2 libxslt
pip install --only-binary=lxml lxml
```

#### **Opción C: Usar Versión Precompilada**
```bash
pip install --only-binary=lxml lxml==4.9.3
```

### 2. **Tests de Seguridad Fallando**

**Problema:**
```
FAILED tests/test_security.py::TestSecurityValidator::test_safe_path_validation
FAILED tests/test_security.py::TestSecurityValidator::test_filename_sanitization
```

**Solución:**
Los tests han sido corregidos. Ejecuta:
```bash
python -m pytest tests/test_security.py -v
```

### 3. **Error de ChromeDriver**

**Problema:**
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH
```

**Soluciones:**

**Fedora:**
```bash
sudo dnf install chromium chromedriver
```

**Ubuntu:**
```bash
sudo apt-get install chromium-browser chromium-chromedriver
```

**macOS:**
```bash
brew install chromium
```

**Manual:**
1. Descargar ChromeDriver desde https://chromedriver.chromium.org/
2. Colocar en PATH o en el directorio del proyecto

### 4. **Permisos de Archivos**

**Problema:**
```
PermissionError: [Errno 13] Permission denied
```

**Solución:**
```bash
# Verificar permisos
ls -la

# Corregir permisos si es necesario
chmod 644 *.py
chmod 755 *.sh
chmod 700 .env  # Si existe
```

### 5. **Variables de Entorno**

**Problema:**
```
ValueError: Variable de entorno requerida no encontrada
```

**Solución:**
```bash
# Crear archivo .env
cp .env.example .env

# Editar con valores apropiados
nano .env
```

### 6. **Importaciones Faltantes**

**Problema:**
```
ModuleNotFoundError: No module named 'utils.security_validator'
```

**Solución:**
```bash
# Verificar estructura de proyecto
python security_check.py

# Reinstalar en modo desarrollo
pip install -e .
```

## 🔍 Diagnóstico Automático

### **Script de Verificación Completa:**
```bash
python security_check.py
```

### **Verificar Instalación:**
```bash
python -c "
import sys
print(f'Python: {sys.version}')

try:
    import lxml
    print('✅ lxml: OK')
except ImportError as e:
    print(f'❌ lxml: {e}')

try:
    import selenium
    print('✅ selenium: OK')
except ImportError as e:
    print(f'❌ selenium: {e}')

try:
    import cv2
    print('✅ opencv: OK')
except ImportError as e:
    print(f'❌ opencv: {e}')

try:
    from utils.security_validator import SecurityValidator
    print('✅ SecurityValidator: OK')
except ImportError as e:
    print(f'❌ SecurityValidator: {e}')
"
```

## 🐛 Debugging Avanzado

### **Logs Detallados:**
```bash
# Ejecutar con logs detallados
python main.py --verbose

# Ver logs de seguridad
tail -f logs/process_log_*.txt
```

### **Modo Debug:**
```python
# Agregar al inicio de main.py para debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **Verificar Configuración:**
```bash
python -c "
import config
print(f'Input Path: {config.DEFAULT_INPUT_PATH}')
print(f'Output Path: {config.DEFAULT_OUTPUT_PATH}')
print(f'Selenium Headless: {config.SELENIUM_HEADLESS}')
"
```

## 📋 Checklist de Verificación

### **Pre-Ejecución:**
- [ ] Dependencias del sistema instaladas
- [ ] Dependencias de Python instaladas
- [ ] ChromeDriver disponible
- [ ] Permisos de archivos correctos
- [ ] Variables de entorno configuradas
- [ ] Tests de seguridad pasan

### **Comando de Verificación Rápida:**
```bash
# Verificación completa
./install_dependencies.sh && \
python security_check.py && \
python -m pytest tests/test_security.py -v && \
echo "✅ Todo listo para usar"
```

## 🆘 Obtener Ayuda

### **Información del Sistema:**
```bash
# Información útil para reportar problemas
echo "Sistema: $(uname -a)"
echo "Python: $(python3 --version)"
echo "Pip: $(pip --version)"
echo "Directorio: $(pwd)"
echo "Archivos: $(ls -la)"
```

### **Logs de Error:**
```bash
# Capturar logs completos
python main.py 2>&1 | tee error_log.txt
```

### **Reinstalación Limpia:**
```bash
# Si todo falla, reinstalación completa
pip uninstall -y -r requirements.txt
rm -rf __pycache__ */__pycache__
./install_dependencies.sh
python security_check.py
```

## 🔄 Mantenimiento

### **Actualización Regular:**
```bash
# Actualizar dependencias
pip list --outdated
pip install --upgrade -r requirements.txt

# Verificar seguridad
python security_check.py
```

### **Limpieza:**
```bash
# Limpiar archivos temporales
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
rm -f temp_*.png
```