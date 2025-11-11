# 🛠️ Utilidades del Sistema

Módulos de utilidad que proporcionan funcionalidades transversales al proyecto.

## 📁 Módulos Disponibles

### 🔒 Seguridad
- **`security_validator.py`** - Validaciones de seguridad (path traversal, SSRF)
- **`pdf_security_analyzer.py`** - Análisis de seguridad específico para PDFs

### 📊 Logging y Monitoreo
- **`logger.py`** - Sistema de logging general
- **`structured_logger.py`** - Logging estructurado para eventos
- **`resource_monitor.py`** - Monitoreo de recursos del sistema
- **`performance_decorator.py`** - Decorador para monitorear funciones

### 💰 Análisis de Costos
- **`cloud_cost_analyzer.py`** - Análisis de costos para despliegue en la nube

### 🖥️ Interfaz y CLI
- **`cli_handler.py`** - Manejo de argumentos de línea de comandos
- **`progress_bar.py`** - Barras de progreso para el usuario
- **`stats_handler.py`** - Manejo de estadísticas y resúmenes

### 📁 Manejo de Archivos
- **`file_handler.py`** - Operaciones seguras con archivos

## 🚀 Uso Rápido

### Monitoreo de Recursos

```python
from utils.resource_monitor import ResourceMonitor

# Crear monitor
monitor = ResourceMonitor(monitoring_interval=0.5)

# Iniciar monitoreo
monitor.start_monitoring()

# Tu código aquí...

# Detener y obtener resumen
monitor.stop_monitoring()
summary = monitor.get_performance_summary()
print(f"CPU promedio: {summary['process_metrics']['cpu_avg']}%")
```

### Análisis de Costos

```python
from utils.cloud_cost_analyzer import CloudCostAnalyzer

analyzer = CloudCostAnalyzer()
analysis = analyzer.analyze_requirements(performance_summary)
analyzer.print_cost_analysis(analysis)
```

### Decorador de Rendimiento

```python
from utils.performance_decorator import monitor_critical_function

@monitor_critical_function
def mi_funcion_importante():
    # Tu código aquí
    pass
```

### Validación de Seguridad

```python
from utils.security_validator import SecurityValidator

# Validar ruta de archivo
if SecurityValidator.validate_file_path(user_path, base_dir):
    # Procesar archivo
    pass

# Validar URL
if SecurityValidator.validate_url(url):
    # Hacer scraping
    pass
```

### Logging Estructurado

```python
from utils.structured_logger import StructuredLogger

logger = StructuredLogger(__name__)

# Log de evento de procesamiento
logger.log_processing_event(
    "archivo.pdf", 
    "SUCCESS", 
    {"qr_count": 3, "duration": 2.5}
)

# Log de evento de seguridad
logger.log_security_event(
    "BLOCKED_URL", 
    {"url": "http://malicious.com", "reason": "Domain not allowed"}
)
```

## 📊 Características Principales

### 🔍 Monitoreo Completo
- **Sistema**: CPU, RAM, I/O disco, red
- **Proceso**: Memoria específica, hilos, descriptores
- **Tiempo real**: Snapshots cada 0.5 segundos
- **Exportación**: JSON detallado para análisis

### 💰 Optimización de Costos
- **AWS, Azure, GCP**: Recomendaciones específicas
- **Escenarios múltiples**: Ocasional, regular, intensivo
- **Cálculo automático**: Costos por hora/mes
- **Comparación**: Mejor precio vs mejor ajuste

### 🛡️ Seguridad Robusta
- **Path Traversal**: Prevención de ataques de directorio
- **SSRF Protection**: Validación de URLs y dominios
- **PDF Analysis**: Detección de contenido malicioso
- **Input Validation**: Sanitización de todas las entradas

### 📈 Logging Avanzado
- **Estructurado**: JSON para análisis automatizado
- **Categorizado**: Procesamiento, seguridad, rendimiento
- **Trazabilidad**: Seguimiento completo de operaciones
- **Auditoría**: Logs para compliance y debugging

## 🎯 Casos de Uso

### Desarrollo Local
```python
# Monitorear rendimiento durante desarrollo
from utils.resource_monitor import start_global_monitoring, stop_global_monitoring

start_global_monitoring(interval=1.0)
# ... tu código de desarrollo ...
summary = stop_global_monitoring()
```

### Producción
```python
# Logging estructurado para producción
from utils.structured_logger import StructuredLogger

logger = StructuredLogger("production")
logger.log_processing_event("batch_job", "STARTED", {"files": 100})
```

### Análisis de Costos
```python
# Antes de desplegar en la nube
from utils.cloud_cost_analyzer import CloudCostAnalyzer

analyzer = CloudCostAnalyzer()
# ... ejecutar carga de trabajo ...
recommendations = analyzer.analyze_requirements(metrics)
```

## 🔧 Configuración

### Variables de Entorno

```bash
# Monitoreo
MONITOR_INTERVAL=0.5
MONITOR_VERBOSE=true

# Logging
LOG_LEVEL=INFO
STRUCTURED_LOG_FORMAT=json

# Seguridad
ALLOWED_DOMAINS=siged.sep.gob.mx,example.com
MAX_FILE_SIZE=50MB
```

### Personalización

```python
# Monitor personalizado
monitor = ResourceMonitor(
    monitoring_interval=0.1,  # 100ms
    export_format='csv'       # CSV en lugar de JSON
)

# Logger personalizado
logger = StructuredLogger(
    module_name="custom",
    log_level="DEBUG",
    output_file="custom.log"
)
```

## 📚 Documentación Detallada

- [📊 Performance Monitoring](../docs/PERFORMANCE_MONITORING.md)
- [☁️ Cloud Deployment](../docs/CLOUD_DEPLOYMENT.md)
- [🔒 Security Guide](../docs/security/)

## 🤝 Contribuir

Para agregar nuevas utilidades:

1. Seguir el patrón de naming existente
2. Incluir docstrings completos
3. Agregar pruebas unitarias
4. Actualizar esta documentación

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) para más detalles.