# 📊 Monitoreo de Rendimiento

Sistema completo de monitoreo de recursos y análisis de rendimiento para optimizar el despliegue en la nube.

## 🎯 Características

### 📈 Monitoreo en Tiempo Real
- **CPU**: Uso promedio, máximo y mínimo del sistema y proceso
- **Memoria**: RAM utilizada, disponible y picos de uso
- **I/O Disco**: Lectura y escritura en MB
- **Red**: Datos enviados y recibidos
- **Procesos**: Conteo de hilos y descriptores de archivo

### 💰 Análisis de Costos en la Nube
- **Recomendaciones automáticas** para AWS, Azure y GCP
- **Cálculo de costos** para diferentes escenarios de uso
- **Comparación de proveedores** y tipos de instancia
- **Optimización de recursos** para minimizar costos

## 🚀 Uso Básico

### Monitoreo Automático

El monitoreo se inicia automáticamente al ejecutar el programa principal:

```bash
python main.py /ruta/pdfs reporte.xlsx
```

**Salida esperada:**
```
🔍 Monitor de recursos iniciado
...procesamiento...
📊 RESUMEN DE RENDIMIENTO
⏱️  Duración total: 45.32s
🖥️  CPU promedio: 23.4%
💾 RAM promedio: 67.8%
🔧 Proceso CPU: 15.2%
📈 Proceso RAM: 245.6MB
🧵 Hilos máx: 8

💰 ANÁLISIS DE COSTOS EN LA NUBE
💡 OPCIONES RECOMENDADAS:
   💸 MÁS BARATA: GCP e2-small ($0.0168/hora)
   🏆 MEJOR AJUSTE: AWS t3.small ($0.0208/hora)
```

### Monitoreo Independiente

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
```

### Demo del Monitor

```bash
python scripts/monitor_demo.py
```

## 📊 Métricas Capturadas

### Sistema Completo

| Métrica | Descripción | Unidad |
|---------|-------------|--------|
| `cpu_percent` | Uso de CPU del sistema | % |
| `memory_percent` | Uso de memoria del sistema | % |
| `memory_used_mb` | Memoria utilizada | MB |
| `memory_available_mb` | Memoria disponible | MB |
| `disk_io_read_mb` | Datos leídos del disco | MB |
| `disk_io_write_mb` | Datos escritos al disco | MB |
| `network_sent_mb` | Datos enviados por red | MB |
| `network_recv_mb` | Datos recibidos por red | MB |
| `process_count` | Número total de procesos | count |
| `thread_count` | Número de hilos activos | count |

### Proceso Específico

| Métrica | Descripción | Unidad |
|---------|-------------|--------|
| `pid` | ID del proceso | number |
| `cpu_percent` | Uso de CPU del proceso | % |
| `memory_percent` | Porcentaje de memoria del proceso | % |
| `memory_rss_mb` | Memoria residente (RSS) | MB |
| `memory_vms_mb` | Memoria virtual (VMS) | MB |
| `num_threads` | Número de hilos del proceso | count |
| `num_fds` | Descriptores de archivo abiertos | count |
| `create_time` | Tiempo de creación del proceso | ISO datetime |
| `status` | Estado del proceso | string |

## 💰 Análisis de Costos

### Recomendaciones Automáticas

El sistema analiza las métricas capturadas y recomienda:

1. **Instancias más baratas** que cumplan los requerimientos
2. **Instancias con mejor ajuste** para el rendimiento
3. **Costos estimados** para diferentes patrones de uso

### Escenarios de Costo

| Escenario | Descripción | Uso Típico |
|-----------|-------------|------------|
| `single_execution` | Una ejecución (tiempo medido) | Pruebas |
| `daily_batch` | Procesamiento diario (1 hora/día) | Producción regular |
| `weekly_batch` | Procesamiento semanal (4 horas/semana) | Procesamiento periódico |
| `always_on` | Instancia siempre activa (24/7) | Servicios continuos |

### Proveedores Soportados

#### AWS (us-east-1)
- **t3.micro** - t3.xlarge (uso general)
- **m5.large** - m5.2xlarge (balanceado)
- **c5.large** - c5.xlarge (CPU optimizado)
- **r5.large** - r5.xlarge (memoria optimizada)

#### Azure
- **B1s** - B2s (básico)
- **D2s_v3** - D4s_v3 (uso general)
- **F2s_v2** - F4s_v2 (CPU optimizado)

#### Google Cloud Platform
- **e2-micro** - e2-standard-4 (eficiente)
- **n1-standard-1** - n1-standard-4 (estándar)

## 🛠️ API del Monitor

### ResourceMonitor

```python
class ResourceMonitor:
    def __init__(self, monitoring_interval: float = 1.0)
    def start_monitoring(self) -> None
    def stop_monitoring(self) -> None
    def get_performance_summary(self) -> Dict
    def export_detailed_metrics(self, output_file: str) -> None
    def log_current_status(self) -> None
```

### CloudCostAnalyzer

```python
class CloudCostAnalyzer:
    def analyze_requirements(self, performance_summary: Dict) -> Dict
    def print_cost_analysis(self, analysis: Dict) -> None
```

### Decorador de Rendimiento

```python
from utils.performance_decorator import monitor_critical_function

@monitor_critical_function
def mi_funcion_critica():
    # Tu código aquí
    pass
```

## 📁 Archivos Generados

### Métricas Detalladas (`*_metrics.json`)

```json
{
  "monitoring_info": {
    "start_time": "2024-01-15T10:30:00",
    "end_time": "2024-01-15T10:35:30",
    "duration_seconds": 330.5,
    "interval_seconds": 0.5
  },
  "system_snapshots": [...],
  "process_metrics": [...],
  "performance_summary": {...}
}
```

### Análisis de Costos (`*_cloud_costs.json`)

```json
{
  "requirements_analysis": {
    "measured_cpu_avg": 23.4,
    "measured_memory_max_mb": 245.6,
    "recommended_vcpus": 2,
    "recommended_memory_gb": 0.4
  },
  "cloud_recommendations": {
    "aws": [...],
    "azure": [...],
    "gcp": [...]
  },
  "cost_analysis": {...}
}
```

## 🎯 Casos de Uso

### 1. Dimensionamiento de Instancias

```bash
# Ejecutar con carga real
python main.py /produccion/pdfs reporte.xlsx

# Revisar recomendaciones
cat reporte_cloud_costs.json | jq '.cost_analysis.best_fit_option'
```

### 2. Optimización de Costos

```bash
# Simular diferentes cargas
python scripts/cost_calculator.py

# Comparar escenarios
ls cost_analysis_*.json
```

### 3. Monitoreo Continuo

```python
from utils.resource_monitor import start_global_monitoring, stop_global_monitoring

# En tu aplicación
start_global_monitoring(interval=1.0)
# ... tu código ...
summary = stop_global_monitoring()
```

## 📈 Interpretación de Resultados

### CPU Usage
- **< 30%**: Instancia sobredimensionada, considera reducir
- **30-70%**: Uso óptimo
- **> 70%**: Considera aumentar vCPUs

### Memory Usage
- **< 50%**: Memoria sobredimensionada
- **50-80%**: Uso óptimo
- **> 80%**: Riesgo de OOM, aumentar memoria

### Fit Score (0-100)
- **90-100**: Excelente ajuste
- **70-89**: Buen ajuste
- **50-69**: Ajuste aceptable
- **< 50**: Mal ajuste, buscar alternativas

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# Intervalo de monitoreo (segundos)
MONITOR_INTERVAL=0.5

# Habilitar logging detallado
MONITOR_VERBOSE=true

# Archivo de salida personalizado
MONITOR_OUTPUT_FILE=custom_metrics.json
```

### Personalización del Monitor

```python
# Monitor personalizado
monitor = ResourceMonitor(monitoring_interval=0.1)  # 100ms

# Configurar logging
monitor.logger.setLevel(logging.DEBUG)

# Exportar en formato personalizado
monitor.export_detailed_metrics("custom_format.json")
```

## 🚨 Troubleshooting

### Problemas Comunes

**Error: "psutil not found"**
```bash
pip install psutil>=5.9.0
```

**Error: "Permission denied"**
```bash
# En Linux, algunos métricas requieren permisos
sudo python main.py /ruta/pdfs reporte.xlsx
```

**Métricas inconsistentes**
```python
# Aumentar intervalo de monitoreo
monitor = ResourceMonitor(monitoring_interval=1.0)
```

### Debugging

```python
# Habilitar logging detallado
import logging
logging.basicConfig(level=logging.DEBUG)

# Verificar estado del monitor
monitor.log_current_status()
```

## 📚 Referencias

- [psutil Documentation](https://psutil.readthedocs.io/)
- [AWS Pricing Calculator](https://calculator.aws)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [GCP Pricing Calculator](https://cloud.google.com/products/calculator)

## 🤝 Contribuir

Para contribuir al sistema de monitoreo:

1. Agregar nuevos proveedores de nube
2. Mejorar algoritmos de recomendación
3. Optimizar captura de métricas
4. Agregar nuevas métricas

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) para más detalles.