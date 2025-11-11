# 📁 Directorio de Ejemplos y Datos de Prueba

## 🎯 **Dónde Colocar tus Archivos**

### **PDFs para Procesar:**
```
data/examples/
├── sample_certificates/     # 👈 COLOCA AQUÍ TUS PDFs
│   ├── certificado1.pdf
│   ├── certificado2.pdf
│   └── certificado3.pdf
└── README.md               # Este archivo
```

### **Reportes Generados:**
```
build/reports/              # 👈 AQUÍ SE GUARDAN LOS RESULTADOS
├── resultado_2025.xlsx
├── validacion_completa.xlsx
└── reporte_seguridad.csv
```

## 🚀 **Comandos de Uso**

### **Procesar PDFs de Ejemplo:**
```bash
# Usar directorio de ejemplos
python -m qr_validator.main data/examples/sample_certificates/ build/reports/resultado.xlsx

# O con el comando make
make run-example
```

### **Procesar tus Propios PDFs:**
```bash
# Crear tu directorio personalizado
mkdir -p data/my_pdfs/

# Copiar tus PDFs
cp /ruta/a/tus/pdfs/*.pdf data/my_pdfs/

# Procesar
python -m qr_validator.main data/my_pdfs/ build/reports/mi_resultado.xlsx
```

## ⚙️ **Configuración de Rutas Seguras**

Las rutas están configuradas para ser seguras dentro del proyecto:
- ✅ `data/` - Archivos de entrada permitidos
- ✅ `build/` - Archivos de salida permitidos
- ❌ Rutas fuera del proyecto - Bloqueadas por seguridad

## 📋 **Estructura Recomendada**

```
data/
├── examples/
│   └── sample_certificates/     # PDFs de ejemplo
├── production/
│   └── certificates_2025/       # PDFs de producción
└── test/
    └── small_batch/            # PDFs para testing
```