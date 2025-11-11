#!/usr/bin/env python3
"""
Demo del monitor de recursos - Ejemplo de uso independiente
"""
import time
import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.resource_monitor import ResourceMonitor


def simulate_workload():
    """Simular carga de trabajo para demostrar el monitoreo"""
    print("🔄 Simulando carga de trabajo...")
    
    # Simular uso de CPU
    for i in range(5):
        print(f"  Iteración {i+1}/5")
        # Operación intensiva en CPU
        result = sum(x**2 for x in range(100000))
        time.sleep(1)
    
    # Simular uso de memoria
    print("📊 Creando estructuras de datos grandes...")
    large_list = [i for i in range(1000000)]
    time.sleep(2)
    
    # Simular I/O
    print("💾 Simulando operaciones de I/O...")
    with open("temp_demo_file.txt", "w") as f:
        for i in range(10000):
            f.write(f"Línea de prueba {i}\n")
    
    # Limpiar archivo temporal
    os.remove("temp_demo_file.txt")
    
    print("✅ Carga de trabajo completada")


def main():
    """Demo principal del monitor"""
    print("="*60)
    print("🔍 DEMO DEL MONITOR DE RECURSOS")
    print("="*60)
    
    # Crear monitor con intervalo de 0.5 segundos
    monitor = ResourceMonitor(monitoring_interval=0.5)
    
    # Iniciar monitoreo
    monitor.start_monitoring()
    print("📈 Monitor iniciado (intervalo: 0.5s)")
    
    try:
        # Ejecutar carga de trabajo
        simulate_workload()
        
        # Esperar un poco más para capturar datos
        time.sleep(2)
        
    finally:
        # Detener monitoreo
        monitor.stop_monitoring()
        print("🛑 Monitor detenido")
    
    # Mostrar resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE RENDIMIENTO")
    print("="*60)
    
    summary = monitor.get_performance_summary()
    
    print(f"⏱️  Duración: {summary['monitoring_duration_seconds']}s")
    print(f"📸 Snapshots: {summary['total_snapshots']}")
    
    print(f"\n🖥️  SISTEMA:")
    sys_metrics = summary['system_metrics']
    print(f"   CPU promedio: {sys_metrics['cpu_avg']}%")
    print(f"   CPU máximo: {sys_metrics['cpu_max']}%")
    print(f"   RAM promedio: {sys_metrics['memory_avg']}%")
    print(f"   RAM máximo: {sys_metrics['memory_max']}%")
    
    print(f"\n🔧 PROCESO:")
    proc_metrics = summary['process_metrics']
    print(f"   PID: {proc_metrics['pid']}")
    print(f"   CPU promedio: {proc_metrics['cpu_avg']}%")
    print(f"   CPU máximo: {proc_metrics['cpu_max']}%")
    print(f"   RAM promedio: {proc_metrics['memory_avg_mb']:.2f}MB")
    print(f"   RAM máximo: {proc_metrics['memory_max_mb']:.2f}MB")
    print(f"   Hilos máximo: {proc_metrics['threads_max']}")
    
    print(f"\n💾 I/O:")
    io_metrics = summary['io_metrics']
    print(f"   Disco leído: {io_metrics['disk_read_mb']:.2f}MB")
    print(f"   Disco escrito: {io_metrics['disk_write_mb']:.2f}MB")
    print(f"   Red enviado: {io_metrics['network_sent_mb']:.2f}MB")
    print(f"   Red recibido: {io_metrics['network_recv_mb']:.2f}MB")
    
    # Exportar métricas detalladas
    output_file = "demo_metrics.json"
    monitor.export_detailed_metrics(output_file)
    print(f"\n📄 Métricas detalladas exportadas a: {output_file}")
    
    print("\n✅ Demo completado")


if __name__ == "__main__":
    main()