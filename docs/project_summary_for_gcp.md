# Resumen Técnico del Proyecto: QR Certificate Validator
**Para Evaluación de Arquitectura en Google Cloud Platform (GCP)**

## 1. Descripción General
Sistema automatizado en Python para el procesamiento por lotes de certificados en formato PDF. El sistema extrae códigos QR, decodifica su contenido y valida la información contra portales gubernamentales (web scraping), generando reportes detallados y análisis de seguridad.

## 2. Stack Tecnológico
- **Lenguaje**: Python 3.8+
- **Visión Computacional**: `OpenCV`, `pyzbar`, `PyMuPDF` (fitz) para manipulación de PDFs e imágenes en memoria.
- **Automatización Web**: `Selenium` con `Chrome/Chromium` (Headless) para validación en tiempo real.
- **Datos**: `Pandas`, `OpenPyXL` para reportes en Excel/JSON.
- **Seguridad**: Detección de patrones maliciosos, validación SSRF, sanitización de paths.

## 3. Arquitectura del Código

### Componentes Principales (`core/`)
- **`pdf_processor.py`**: Maneja la conversión de PDF a imagen en memoria (sin archivos intermedios en disco).
- **`qr_detector.py`**: Implementa lógica de "Early Exit" probando múltiples técnicas de visión (Grayscale, Thresholding, Adaptive) hasta encontrar un QR válido.
- **`web_scraper.py`**: Cliente Selenium robusto con rotación de User-Agents y manejo de Timeouts escalonados.
- **`validator.py`**: Lógica de negocio para comparar datos extraídos del QR vs datos obtenidos de la web.

### Utilidades Críticas (`utils/`)
- **`security_validator.py`**: Firewall interno. Valida URLs antes de hacer requests (evita SSRF), sanitiza nombres de archivos y previene Path Traversal.
- **`resource_monitor.py`**: Monitoreo en tiempo real de CPU/RAM durante la ejecución.
- **`cloud_cost_analyzer.py`**: Estima costos de ejecución basado en el consumo de recursos detectado.

### Entrada/Salida
- **Input**: Directorio local o path con archivos `.pdf`.
- **Output**: Archivo Excel (`.xlsx`) y JSON (`.json`) con resultados, métricas y logs.

## 4. Consideraciones para Despliegue en GCP

### Dependencias de Sistema (Reto Principal)
El proyecto requiere un entorno con:
- `python3`
- `libxml2-devel`, `libxslt-devel` (para lxml)
- **Google Chrome** o **Chromium** instalado.
- **ChromeDriver** compatible.

### Modelo de Ejecución
- El script es **Stateless** por archivo: Toma un PDF, procesa y devuelve resultado.
- Ideal para procesamiento asíncrono/por eventos.
- **Uso de Recursos**:
    - **CPU**: Intensivo durante la detección de QR (OpenCV).
    - **RAM**: Moderado (procesamiento de imágenes en memoria).
    - **Network**: Tráfico de salida para Selenium (validación web).

### Seguridad
- El código ya incluye validación de dominios permitidos (whitelist).
- Maneja secretos vía variables de entorno (`.env`).
- No requiere base de datos persistente (todo se reporta en archivos de salida).

## 5. Preguntas Clave para el Arquitecto Cloud
1.  Dado que requiere **Chrome Headless**, ¿es mejor usar **Cloud Run** con un contenedor custom o **GKE**?
2.  ¿Cómo manejar la escalabilidad de Selenium (que consume mucha RAM) si llegan 1000 PDFs simultáneos? ¿Cola de mensajes (Pub/Sub)?
3.  ¿Cuál es la mejor opción de almacenamiento para los PDFs de entrada y los reportes de salida? (Probablemente **GCS**).
4.  ¿Cómo integrar el script `main.py` para que se dispare automáticamente al subir un archivo a un Bucket? (Cloud Functions vs Eventarc + Cloud Run).
