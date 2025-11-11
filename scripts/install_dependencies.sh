#!/bin/bash
# Script de instalación de dependencias para QR Certificate Validator

echo "🔧 Instalando dependencias del sistema para QR Certificate Validator..."

# Detectar sistema operativo
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v dnf &> /dev/null; then
        # Fedora/RHEL/CentOS
        echo "📦 Detectado Fedora/RHEL - Instalando dependencias del sistema..."
        sudo dnf install -y python3-devel libxml2-devel libxslt-devel gcc gcc-c++ chromium chromedriver
    elif command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        echo "📦 Detectado Ubuntu/Debian - Instalando dependencias del sistema..."
        sudo apt-get update
        sudo apt-get install -y python3-dev libxml2-dev libxslt-dev build-essential chromium-browser chromium-chromedriver
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        echo "📦 Detectado Arch Linux - Instalando dependencias del sistema..."
        sudo pacman -S --noconfirm python libxml2 libxslt gcc chromium
    else
        echo "⚠️  Sistema Linux no reconocido. Instala manualmente:"
        echo "   - python3-dev/python3-devel"
        echo "   - libxml2-dev/libxml2-devel"
        echo "   - libxslt-dev/libxslt-devel"
        echo "   - gcc/build-essential"
        echo "   - chromium/chromium-browser"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "📦 Detectado macOS - Instalando dependencias..."
    if command -v brew &> /dev/null; then
        brew install libxml2 libxslt chromium
    else
        echo "⚠️  Homebrew no encontrado. Instala Homebrew primero:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
else
    echo "❌ Sistema operativo no soportado: $OSTYPE"
    exit 1
fi

echo "🐍 Instalando dependencias de Python..."

# Actualizar pip
python3 -m pip install --upgrade pip

# Instalar dependencias básicas primero
python3 -m pip install wheel setuptools

# Instalar lxml con opciones específicas para evitar errores de compilación
echo "📦 Instalando lxml..."
python3 -m pip install --only-binary=lxml lxml || {
    echo "⚠️  Instalación binaria falló, intentando compilar desde fuente..."
    python3 -m pip install lxml
}

# Instalar resto de dependencias
echo "📦 Instalando resto de dependencias..."
python3 -m pip install -r requirements.txt

echo "✅ Instalación completada!"
echo ""
echo "🔍 Verificando instalación..."
python3 -c "import lxml; print('✅ lxml instalado correctamente')" || echo "❌ Error con lxml"
python3 -c "import selenium; print('✅ selenium instalado correctamente')" || echo "❌ Error con selenium"
python3 -c "import cv2; print('✅ opencv instalado correctamente')" || echo "❌ Error con opencv"

echo ""
echo "🚀 Para verificar que todo funciona:"
echo "   python security_check.py"
echo "   python -m pytest tests/test_security.py -v"