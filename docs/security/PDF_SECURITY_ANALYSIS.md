# Análisis de Seguridad PDF

## Descripción

El módulo de análisis de seguridad PDF protege el entorno universitario detectando contenido malicioso embebido en archivos PDF antes del procesamiento de QR.

## Características de Seguridad

### 🔍 **Detección de Elementos Maliciosos**

| Elemento | Nivel de Riesgo | Descripción |
|----------|----------------|-------------|
| `/JavaScript`, `/JS` | **CRÍTICO** | Código JavaScript embebido |
| `/Launch` | **CRÍTICO** | Ejecución de programas externos |
| `/OpenAction`, `/AA` | **ALTO** | Acciones automáticas al abrir |
| `/SubmitForm`, `/ImportData` | **ALTO** | Envío de datos a servidores |
| `/RichMedia`, `/3D` | **ALTO** | Contenido multimedia complejo |
| `/EmbeddedFile` | **MEDIO** | Archivos embebidos |
| `/XFA` | **MEDIO** | Formularios XML avanzados |
| `/GoToR` | **MEDIO** | Enlaces a recursos remotos |
| `/URI` | **BAJO** | Enlaces web simples |

### 🚨 **Patrones Sospechosos Detectados**

- **JavaScript malicioso**: `eval()`, `document.write`, `unescape()`
- **Ejecución de comandos**: `cmd.exe`, `powershell`, `WScript.Shell`
- **Objetos ActiveX**: `ActiveXObject`
- **URLs externas**: Enlaces a sitios web

### 📊 **Niveles de Riesgo**

| Nivel | Puntuación | Acción Recomendada |
|-------|------------|-------------------|
| **SAFE** | 0 | ✅ Procesar normalmente |
| **LOW** | 1-24 | 🟡 Permitir con monitoreo |
| **MEDIUM** | 25-49 | 🟠 Revisar con precaución |
| **HIGH** | 50-99 | 🔴 Enviar a cuarentena |
| **CRITICAL** | 100+ | 💀 Bloquear completamente |

## Uso del Módulo

### 1. **Integración Automática**

El análisis se ejecuta automáticamente en el procesamiento principal:

```bash
python main.py
```

Los PDFs riesgosos se marcan y no se procesan para QR.

### 2. **Análisis Independiente**

Para analizar PDFs sin procesamiento de QR:

```bash
# Archivo individual
python security_scan.py certificado.pdf

# Directorio completo
python security_scan.py /ruta/a/pdfs/
```

### 3. **Programático**

```python
from utils.pdf_security_analyzer import PDFSecurityAnalyzer

analyzer = PDFSecurityAnalyzer()
result = analyzer.analyze_pdf_security("archivo.pdf")

# Verificar seguridad
if analyzer.is_safe_pdf(result):
    print("PDF seguro para procesar")
elif analyzer.should_quarantine(result):
    print("PDF debe ir a cuarentena")
```

## Salida del Análisis

### **Reporte de Seguridad**

```json
{
  "file_info": {
    "filename": "certificado.pdf",
    "size_mb": 2.5,
    "sha256": "abc123..."
  },
  "risk_assessment": {
    "overall_risk": "MEDIUM",
    "risk_score": 35,
    "threats": [
      "MEDIO: /EmbeddedFile encontrado 1 veces",
      "Patrón sospechoso: External URLs"
    ],
    "recommendation": "PRECAUCIÓN - Monitorear"
  },
  "raw_analysis": {
    "risky_elements_found": {
      "/EmbeddedFile": {
        "count": 1,
        "risk_level": "MEDIUM"
      }
    },
    "external_references": [
      "https://ejemplo.com/validar"
    ]
  }
}
```

### **Columnas en Excel**

El reporte principal incluye columnas de seguridad:

- `security_status`: SAFE, QUARANTINE
- `security_risk`: Nivel de riesgo detectado
- `security_threats`: Amenazas encontradas
- `security_recommendation`: Acción recomendada

## Casos de Uso Universitarios

### 📚 **Certificados de Estudiantes**
- Detecta PDFs con JavaScript malicioso
- Identifica formularios que podrían robar datos
- Bloquea archivos con ejecutables embebidos

### 🏛️ **Documentos Administrativos**
- Previene ataques de phishing via PDF
- Detecta intentos de exfiltración de datos
- Identifica documentos con contenido sospechoso

### 🔒 **Protección Institucional**
- Evita comprometer sistemas internos
- Mantiene logs de seguridad auditables
- Proporciona reportes para compliance

## Configuración de Seguridad

### **Personalizar Elementos de Riesgo**

Editar `utils/pdf_security_analyzer.py`:

```python
RISKY_ELEMENTS = {
    '/JavaScript': 'CRITICAL',
    '/CustomElement': 'HIGH',  # Agregar nuevo elemento
    # ...
}
```

### **Ajustar Umbrales de Riesgo**

Modificar puntuaciones en `_assess_risk()`:

```python
if risk_level == 'CRITICAL':
    risk_score += 50 * count  # Ajustar peso
```

## Logs de Seguridad

Todos los eventos se registran en logs estructurados:

```json
{
  "timestamp": "2025-01-10T18:30:00",
  "event_type": "PDF_SECURITY_SCAN", 
  "data": {
    "file": "certificado.pdf",
    "risk_level": "HIGH",
    "threats_found": 3
  }
}
```

## Mejores Prácticas

### ✅ **Recomendaciones**

1. **Ejecutar análisis antes del procesamiento**
2. **Revisar manualmente PDFs de riesgo MEDIUM+**
3. **Mantener logs de seguridad para auditorías**
4. **Actualizar patrones de detección regularmente**
5. **Capacitar personal en identificación de amenazas**

### ⚠️ **Limitaciones**

- No detecta malware cifrado o ofuscado avanzado
- Requiere actualización manual de patrones
- Puede generar falsos positivos con PDFs legítimos complejos

## Integración con Sistemas Universitarios

### **SIEM Integration**
Los logs estructurados pueden enviarse a sistemas SIEM institucionales.

### **Quarantine Workflow**
PDFs riesgosos pueden moverse automáticamente a carpetas de cuarentena.

### **Notification System**
Alertas automáticas para administradores cuando se detectan amenazas críticas.