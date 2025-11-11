# 🔧 Scripts de Utilidad

Colección de scripts para automatizar tareas comunes, demos y configuración del proyecto.

## 📁 Scripts Disponibles

### 🚀 Configuración y Setup
- **`install_dependencies.sh`** - Instalación automática de dependencias del sistema
- **`setup_dev_env.sh`** - Configuración completa del entorno de desarrollo
- **`setup_test_data.sh`** - Creación de datos de prueba

### 🔒 Seguridad
- **`security_check.py`** - Verificación completa de seguridad del proyecto

### 📊 Monitoreo y Análisis
- **`monitor_demo.py`** - Demostración del sistema de monitoreo de recursos
- **`cost_calculator.py`** - Calculadora de costos para despliegue en la nube

## 🎯 Uso de Scripts

### Configuración Inicial

```bash
# Instalación completa automática
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh

# Configurar entorno de desarrollo
chmod +x scripts/setup_dev_env.sh
./scripts/setup_dev_env.sh

# Crear datos de prueba
chmod +x scripts/setup_test_data.sh
./scripts/setup_test_data.sh
```

### Verificación de Seguridad

```bash
# Análisis completo de seguridad
python scripts/security_check.py

# Verificación específica de un directorio
python scripts/security_check.py --path /ruta/especifica
```

### Análisis de Rendimiento

```bash
# Demo del monitor de recursos
python scripts/monitor_demo.py

# Calculadora de costos en la nube
python scripts/cost_calculator.py
```

## 📊 Monitor Demo (`monitor_demo.py`)

### Características
- **Simulación de carga** de trabajo realista
- **Métricas en tiempo real** de CPU, RAM, I/O
- **Resumen detallado** de rendimiento
- **Exportación automática** de métricas

### Salida Esperada
```
🔍 DEMO DEL MONITOR DE RECURSOS
📈 Monitor iniciado (intervalo: 0.5s)
🔄 Simulando carga de trabajo...
  Iteración 1/5
  ...
📊 RESUMEN DE RENDIMIENTO
⏱️  Duración: 15.3s
🖥️  SISTEMA:
   CPU promedio: 45.2%
   RAM promedio: 67.8%
🔧 PROCESO:
   CPU promedio: 23.4%
   RAM máximo: 245.6MB
```

## 💰 Calculadora de Costos (`cost_calculator.py`)

### Escenarios Simulados

#### 🟢 Carga Ligera
- **10 PDFs**, uso ocasional
- **CPU**: 15% promedio, 35% máximo
- **RAM**: 150MB promedio, 200MB máximo
- **Duración**: 2 minutos

#### 🟡 Carga Media
- **100 PDFs**, uso regular
- **CPU**: 45% promedio, 75% máximo
- **RAM**: 400MB promedio, 600MB máximo
- **Duración**: 30 minutos

#### 🔴 Carga Pesada
- **500+ PDFs**, uso intensivo
- **CPU**: 70% promedio, 95% máximo
- **RAM**: 800MB promedio, 1.2GB máximo
- **Duración**: 2 horas

### Recomendaciones Generadas

```
💡 RECOMENDACIONES GENERALES:
   • Para uso ocasional: AWS t3.small o GCP e2-small
   • Para uso regular: AWS t3.medium o Azure B2s
   • Para uso intensivo: AWS m5.large o Azure D2s_v3

💰 ESTRATEGIAS DE AHORRO:
   • Instancias reservadas: 30-60% descuento
   • Instancias spot: 50-90% descuento
   • Auto-scaling para cargas variables
```

## 🔒 Security Check (`security_check.py`)

### Verificaciones Realizadas

#### Dependencias
- **Vulnerabilidades conocidas** en packages
- **Versiones desactualizadas** de librerías
- **Licencias incompatibles**

#### Código Fuente
- **Hardcoded credentials** en archivos
- **SQL injection** patterns
- **Path traversal** vulnerabilities
- **Insecure imports** y funciones

#### Configuración
- **Permisos de archivos** incorrectos
- **Variables de entorno** sensibles
- **Configuraciones inseguras**

### Salida del Análisis

```
🔒 ANÁLISIS DE SEGURIDAD COMPLETADO
=====================================
✅ Dependencias: 0 vulnerabilidades críticas
⚠️  Código fuente: 2 warnings encontrados
✅ Configuración: Segura
✅ Archivos: Permisos correctos

📋 RECOMENDACIONES:
   • Actualizar urllib3 a versión >= 2.0.7
   • Revisar hardcoded timeout en config.py:45
```

## 🛠️ Scripts de Setup

### `install_dependencies.sh`

```bash
#!/bin/bash
# Instalación automática para diferentes sistemas

# Detectar sistema operativo
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install -y python3-pip libxml2-dev libxslt-dev chromium-browser
    
    # Fedora/RHEL
    if command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip libxml2-devel libxslt-devel chromium
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    brew install libxml2 libxslt
    brew install --cask google-chrome
fi

# Instalar dependencias Python
pip3 install -r requirements.txt
```

### `setup_dev_env.sh`

```bash
#!/bin/bash
# Configuración completa del entorno de desarrollo

echo "🚀 Configurando entorno de desarrollo..."

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configurar pre-commit hooks
pre-commit install

# Crear directorios necesarios
mkdir -p data/examples data/production logs output

# Copiar configuración de ejemplo
cp .env.example .env

echo "✅ Entorno configurado correctamente"
```

### `setup_test_data.sh`

```bash
#!/bin/bash
# Crear estructura de datos de prueba

echo "📁 Creando datos de prueba..."

# Crear directorios
mkdir -p data/examples/{valid,invalid,malicious}
mkdir -p tests/fixtures

# Crear archivos de ejemplo (simulados)
touch data/examples/valid/certificate_001.pdf
touch data/examples/valid/certificate_002.pdf
touch data/examples/invalid/corrupted.pdf
touch data/examples/malicious/suspicious.pdf

echo "✅ Datos de prueba creados"
```

## 🎯 Casos de Uso

### Desarrollo Local

```bash
# Setup inicial completo
./scripts/setup_dev_env.sh

# Verificar que todo funciona
python scripts/monitor_demo.py
python scripts/security_check.py
```

### CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
- name: Security Check
  run: python scripts/security_check.py --fail-on-error

- name: Performance Baseline
  run: python scripts/monitor_demo.py --export-baseline
```

### Análisis Pre-Despliegue

```bash
# Analizar costos antes de desplegar
python scripts/cost_calculator.py > cost_analysis.txt

# Verificar seguridad
python scripts/security_check.py --detailed-report
```

## 🔧 Personalización

### Agregar Nuevos Scripts

```bash
# Crear nuevo script
touch scripts/mi_script.py
chmod +x scripts/mi_script.py

# Template básico
cat > scripts/mi_script.py << 'EOF'
#!/usr/bin/env python3
"""
Descripción del script
"""
import sys
import os

# Agregar directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Función principal"""
    print("Mi script personalizado")

if __name__ == "__main__":
    main()
EOF
```

### Configurar Scripts

```bash
# Variables de entorno para scripts
export SCRIPT_VERBOSE=true
export SCRIPT_OUTPUT_DIR=./output
export SCRIPT_LOG_LEVEL=DEBUG
```

## 📚 Documentación Relacionada

- [📊 Performance Monitoring](../docs/PERFORMANCE_MONITORING.md)
- [☁️ Cloud Deployment](../docs/CLOUD_DEPLOYMENT.md)
- [🔒 Security Guide](../docs/security/)
- [🤝 Contributing](../CONTRIBUTING.md)

## 🚨 Troubleshooting

### Problemas Comunes

**Script no ejecutable**
```bash
chmod +x scripts/nombre_script.sh
```

**Dependencias faltantes**
```bash
./scripts/install_dependencies.sh
```

**Permisos insuficientes**
```bash
# Algunos scripts pueden requerir sudo
sudo ./scripts/setup_system.sh
```

## 🤝 Contribuir

Para agregar nuevos scripts:

1. Seguir el template de estructura
2. Incluir documentación en docstring
3. Agregar a este README
4. Incluir pruebas si es aplicable

¡Los scripts hacen la vida más fácil! 🚀