#!/bin/bash
echo "🔧 Configurando entorno de desarrollo para QR Certificate Validator..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instala Python 3.8+ primero."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip setuptools wheel

# Instalar dependencias del sistema
echo "🛠️ Instalando dependencias del sistema..."
./scripts/install_dependencies.sh

# Instalar paquete en modo desarrollo
echo "📦 Instalando paquete en modo desarrollo..."
pip install -e ".[dev]"

# Configurar pre-commit hooks
echo "🪝 Configurando pre-commit hooks..."
pip install pre-commit
pre-commit install

# Crear directorios necesarios
echo "📁 Creando directorios necesarios..."
mkdir -p build/{logs,temp,reports}
mkdir -p data/examples
mkdir -p tests/fixtures

# Copiar configuración de ejemplo
if [ ! -f ".env" ]; then
    echo "⚙️ Copiando configuración de ejemplo..."
    cp config/.env.example .env
    echo "✏️ Edita el archivo .env con tus configuraciones"
fi

# Verificar instalación
echo "🔍 Verificando instalación..."
python -c "import qr_validator; print(f'✅ QR Validator {qr_validator.__version__} instalado correctamente')"

# Ejecutar tests básicos
echo "🧪 Ejecutando tests básicos..."
python -m pytest tests/unit/test_security.py -v

echo ""
echo "✅ Entorno de desarrollo configurado correctamente!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Activar entorno: source venv/bin/activate"
echo "2. Editar configuración: nano .env"
echo "3. Ejecutar tests: make test"
echo "4. Ver ayuda: make help"
echo ""
echo "🚀 Ejemplo de uso:"
echo "   make run-example"