#!/bin/bash
echo "📁 Configurando datos de prueba para QR Certificate Validator..."

# Crear directorios si no existen
mkdir -p data/examples/sample_certificates
mkdir -p data/production/certificates_2025
mkdir -p data/test/small_batch
mkdir -p build/reports

echo "✅ Directorios creados:"
echo "  📂 data/examples/sample_certificates/     - Coloca aquí tus PDFs de ejemplo"
echo "  📂 data/production/certificates_2025/     - PDFs de producción"
echo "  📂 data/test/small_batch/                 - PDFs para testing rápido"
echo "  📂 build/reports/                         - Reportes generados"

# Crear archivo de ejemplo con instrucciones
cat > data/examples/sample_certificates/INSTRUCCIONES.txt << 'EOF'
📋 INSTRUCCIONES PARA USAR TUS PDFs

1. Copia tus archivos PDF aquí:
   cp /ruta/a/tus/pdfs/*.pdf data/examples/sample_certificates/

2. Ejecuta el procesamiento:
   python -m qr_validator.main data/examples/sample_certificates/ build/reports/resultado.xlsx

3. O usa el comando make:
   make run-example

4. Los resultados aparecerán en:
   build/reports/

📁 ESTRUCTURA RECOMENDADA:
data/examples/sample_certificates/
├── certificado_1.pdf
├── certificado_2.pdf
├── certificado_3.pdf
└── más_certificados.pdf

🔒 SEGURIDAD:
- Solo se procesan archivos dentro del directorio del proyecto
- Extensiones permitidas: .pdf, .xlsx, .csv, .json, .txt, .log
- Tamaño máximo por archivo: 100MB
EOF

# Crear configuración de ejemplo
cat > config/.env.example << 'EOF'
# Configuración de QR Certificate Validator

# Rutas (relativas al proyecto)
DEFAULT_INPUT_PATH=data/examples/sample_certificates
DEFAULT_OUTPUT_PATH=build/reports

# Selenium
SELENIUM_TIMEOUT_SHORT=8
SELENIUM_TIMEOUT_MEDIUM=14
SELENIUM_TIMEOUT_LONG=18
SELENIUM_HEADLESS=true

# Procesamiento
MAX_WORKERS=4
ZOOM_LEVELS=2,3,4,5,6
DPI_LEVELS=150,200,300

# Logging
LOG_LEVEL=INFO
LOG_FILE=build/logs/process_log.txt
EOF

# Copiar configuración si no existe .env
if [ ! -f ".env" ]; then
    cp config/.env.example .env
    echo "✅ Archivo .env creado con configuración por defecto"
else
    echo "ℹ️  Archivo .env ya existe, no se sobrescribió"
fi

echo ""
echo "🎯 PRÓXIMOS PASOS:"
echo "1. Copia tus PDFs a: data/examples/sample_certificates/"
echo "2. Ejecuta: make run-example"
echo "3. Revisa resultados en: build/reports/"
echo ""
echo "📋 COMANDOS ÚTILES:"
echo "  make help           - Ver todos los comandos"
echo "  make test           - Ejecutar tests"
echo "  make setup-dev      - Configurar entorno completo"