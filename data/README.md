# 📁 Data Directory

Directorio para almacenar archivos PDF de entrada organizados por propósito.

## 📂 Estructura

```
data/
├── examples/              # PDFs de ejemplo y demos
│   └── sample_certificates/   # Certificados de muestra
└── production/           # PDFs de producción (datos reales)
    └── certificates_2025/    # Certificados del año 2025
```

## 🎯 Uso de Carpetas

### 📋 `examples/sample_certificates/`
- **Propósito**: PDFs de ejemplo para pruebas y demos
- **Contenido**: 6 certificados de muestra incluidos
- **Uso**: `python main.py data/examples/sample_certificates/ demo.xlsx`

### 🏭 `production/certificates_2025/`
- **Propósito**: Certificados reales para procesamiento en producción
- **Contenido**: Coloca aquí tus 500+ certificados
- **Uso**: `python main.py data/production/certificates_2025/ reporte_2025.xlsx`

## 📝 Instrucciones

### Para Procesar Certificados de Ejemplo
```bash
# Los ejemplos ya están incluidos, solo ejecuta:
python main.py data/examples/sample_certificates/ ejemplo_reporte.xlsx
```

### Para Procesar Certificados de Producción
```bash
# 1. Copia tus PDFs a la carpeta de producción
cp /ruta/a/tus/pdfs/*.pdf data/production/certificates_2025/

# 2. Ejecuta el procesamiento
python main.py data/production/certificates_2025/ reporte_produccion.xlsx
```

### Para Organizar por Lotes (Opcional)
```bash
# Crear subcarpetas por período
mkdir -p data/production/lote_enero
mkdir -p data/production/lote_febrero

# Mover PDFs por lotes
mv certificados_enero_*.pdf data/production/lote_enero/
mv certificados_febrero_*.pdf data/production/lote_febrero/

# Procesar cada lote
python main.py data/production/lote_enero/ reporte_enero.xlsx
python main.py data/production/lote_febrero/ reporte_febrero.xlsx
```

## ⚠️ Consideraciones

### Seguridad
- **No subir PDFs reales** a repositorios públicos
- **Usar .gitignore** para excluir `data/production/`
- **Verificar permisos** de archivos antes del procesamiento

### Rendimiento
- **Lotes recomendados**: 50-100 PDFs por carpeta para mejor control
- **Espacio en disco**: ~1-5MB por PDF típico
- **Tiempo estimado**: 2-3 segundos por PDF con validación web

### Formatos Soportados
- ✅ **PDF estándar** (.pdf)
- ✅ **PDFs con QR embebidos**
- ✅ **Múltiples páginas** (busca en todas)
- ❌ **Archivos corruptos** (se omiten con log de error)

## 🔍 Ejemplos Incluidos

Los certificados de ejemplo incluyen:
- **Diferentes formatos** de QR
- **Varios tipos de datos** (nombres, promedios, folios)
- **URLs de validación** reales para testing
- **Casos edge** para pruebas robustas

Ver `data/examples/sample_certificates/INSTRUCCIONES.txt` para más detalles.