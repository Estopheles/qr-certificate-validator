#!/usr/bin/env python3
"""
Monitor de recursos del sistema usando psutil
Espía el uso de CPU, RAM, tiempos de trabajo y rendimiento del proyecto
"""
import os
import time
import psutil
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from utils.structured_logger import StructuredLogger


@dataclass
class ResourceSnapshot:
    """Instantánea de recursos del sistema"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_io_read_mb: float
    disk_io_write_mb: float
    network_sent_mb: float
    network_recv_mb: float
    process_count: int
    thread_count: int


@dataclass
class ProcessMetrics:
    """Métricas específicas del proceso actual"""
    pid: int
    cpu_percent: float
    memory_percent: float
    memory_rss_mb: float
    memory_vms_mb: float
    num_threads: int
    num_fds: int
    create_time: str
    status: str


class ResourceMonitor:
    """Monitor de recursos del sistema y proceso"""
    
    def __init__(self, monitoring_interval: float = 1.0):
        """
        Inicializar monitor de recursos
        
        Args:
            monitoring_interval: Intervalo de monitoreo en segundos
        """
        self.monitoring_interval = monitoring_interval
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.snapshots: List[ResourceSnapshot] = []
        self.process_metrics: List[ProcessMetrics] = []
        self.start_time = time.time()
        self.logger = StructuredLogger(__name__)
        
        # Obtener proceso actual
        self.current_process = psutil.Process()
        
        # Métricas iniciales para calcular deltas
        self._initial_disk_io = psutil.disk_io_counters()
        self._initial_network_io = psutil.net_io_counters()
        
    def start_monitoring(self) -> None:
        """Iniciar monitoreo en hilo separado"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.log_processing_event(
            "resource_monitor", 
            "MONITORING_STARTED", 
            {"interval": self.monitoring_interval}
        )
        
    def stop_monitoring(self) -> None:
        """Detener monitoreo"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
            
        self.logger.log_processing_event(
            "resource_monitor", 
            "MONITORING_STOPPED", 
            {"total_snapshots": len(self.snapshots)}
        )
        
    def _monitor_loop(self) -> None:
        """Loop principal de monitoreo"""
        while self.is_monitoring:
            try:
                # Capturar snapshot del sistema
                system_snapshot = self._capture_system_snapshot()
                self.snapshots.append(system_snapshot)
                
                # Capturar métricas del proceso
                process_metrics = self._capture_process_metrics()
                self.process_metrics.append(process_metrics)
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                self.logger.log_processing_event(
                    "resource_monitor", 
                    "MONITORING_ERROR", 
                    {"error": str(e)}
                )
                time.sleep(self.monitoring_interval)
                
    def _capture_system_snapshot(self) -> ResourceSnapshot:
        """Capturar snapshot del sistema"""
        # CPU y memoria
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        
        # I/O de disco
        disk_io = psutil.disk_io_counters()
        disk_read_mb = (disk_io.read_bytes - self._initial_disk_io.read_bytes) / (1024 * 1024)
        disk_write_mb = (disk_io.write_bytes - self._initial_disk_io.write_bytes) / (1024 * 1024)
        
        # I/O de red
        network_io = psutil.net_io_counters()
        network_sent_mb = (network_io.bytes_sent - self._initial_network_io.bytes_sent) / (1024 * 1024)
        network_recv_mb = (network_io.bytes_recv - self._initial_network_io.bytes_recv) / (1024 * 1024)
        
        return ResourceSnapshot(
            timestamp=datetime.now().isoformat(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / (1024 * 1024),
            memory_available_mb=memory.available / (1024 * 1024),
            disk_io_read_mb=disk_read_mb,
            disk_io_write_mb=disk_write_mb,
            network_sent_mb=network_sent_mb,
            network_recv_mb=network_recv_mb,
            process_count=len(psutil.pids()),
            thread_count=threading.active_count()
        )
        
    def _capture_process_metrics(self) -> ProcessMetrics:
        """Capturar métricas del proceso actual"""
        try:
            memory_info = self.current_process.memory_info()
            
            return ProcessMetrics(
                pid=self.current_process.pid,
                cpu_percent=self.current_process.cpu_percent(),
                memory_percent=self.current_process.memory_percent(),
                memory_rss_mb=memory_info.rss / (1024 * 1024),
                memory_vms_mb=memory_info.vms / (1024 * 1024),
                num_threads=self.current_process.num_threads(),
                num_fds=self.current_process.num_fds() if hasattr(self.current_process, 'num_fds') else 0,
                create_time=datetime.fromtimestamp(self.current_process.create_time()).isoformat(),
                status=self.current_process.status()
            )
        except psutil.NoSuchProcess:
            # Proceso terminado, crear métricas vacías
            return ProcessMetrics(
                pid=0, cpu_percent=0.0, memory_percent=0.0,
                memory_rss_mb=0.0, memory_vms_mb=0.0, num_threads=0,
                num_fds=0, create_time="", status="terminated"
            )
            
    def get_performance_summary(self) -> Dict:
        """Obtener resumen de rendimiento"""
        if not self.snapshots or not self.process_metrics:
            return {"error": "No hay datos de monitoreo disponibles"}
            
        # Calcular estadísticas del sistema
        cpu_values = [s.cpu_percent for s in self.snapshots]
        memory_values = [s.memory_percent for s in self.snapshots]
        
        # Calcular estadísticas del proceso
        process_cpu_values = [p.cpu_percent for p in self.process_metrics]
        process_memory_values = [p.memory_rss_mb for p in self.process_metrics]
        
        total_time = time.time() - self.start_time
        
        return {
            "monitoring_duration_seconds": round(total_time, 2),
            "total_snapshots": len(self.snapshots),
            "system_metrics": {
                "cpu_avg": round(sum(cpu_values) / len(cpu_values), 2),
                "cpu_max": round(max(cpu_values), 2),
                "cpu_min": round(min(cpu_values), 2),
                "memory_avg": round(sum(memory_values) / len(memory_values), 2),
                "memory_max": round(max(memory_values), 2),
                "memory_min": round(min(memory_values), 2),
            },
            "process_metrics": {
                "cpu_avg": round(sum(process_cpu_values) / len(process_cpu_values), 2),
                "cpu_max": round(max(process_cpu_values), 2),
                "memory_avg_mb": round(sum(process_memory_values) / len(process_memory_values), 2),
                "memory_max_mb": round(max(process_memory_values), 2),
                "threads_max": max([p.num_threads for p in self.process_metrics]),
                "pid": self.current_process.pid
            },
            "io_metrics": {
                "disk_read_mb": round(self.snapshots[-1].disk_io_read_mb, 2),
                "disk_write_mb": round(self.snapshots[-1].disk_io_write_mb, 2),
                "network_sent_mb": round(self.snapshots[-1].network_sent_mb, 2),
                "network_recv_mb": round(self.snapshots[-1].network_recv_mb, 2)
            }
        }
        
    def export_detailed_metrics(self, output_file: str) -> None:
        """Exportar métricas detalladas a archivo JSON"""
        import json
        
        data = {
            "monitoring_info": {
                "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": time.time() - self.start_time,
                "interval_seconds": self.monitoring_interval
            },
            "system_snapshots": [asdict(snapshot) for snapshot in self.snapshots],
            "process_metrics": [asdict(metrics) for metrics in self.process_metrics],
            "performance_summary": self.get_performance_summary()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        self.logger.log_processing_event(
            "resource_monitor", 
            "METRICS_EXPORTED", 
            {"output_file": output_file, "snapshots": len(self.snapshots)}
        )
        
    def log_current_status(self) -> None:
        """Loggear estado actual del sistema"""
        if not self.snapshots:
            return
            
        latest_snapshot = self.snapshots[-1]
        latest_process = self.process_metrics[-1] if self.process_metrics else None
        
        self.logger.log_processing_event(
            "resource_monitor", 
            "CURRENT_STATUS", 
            {
                "system_cpu": latest_snapshot.cpu_percent,
                "system_memory": latest_snapshot.memory_percent,
                "process_cpu": latest_process.cpu_percent if latest_process else 0,
                "process_memory_mb": latest_process.memory_rss_mb if latest_process else 0,
                "process_threads": latest_process.num_threads if latest_process else 0
            }
        )


# Instancia global del monitor
_global_monitor: Optional[ResourceMonitor] = None


def get_global_monitor() -> ResourceMonitor:
    """Obtener instancia global del monitor"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = ResourceMonitor()
    return _global_monitor


def start_global_monitoring(interval: float = 1.0) -> None:
    """Iniciar monitoreo global"""
    monitor = get_global_monitor()
    monitor.monitoring_interval = interval
    monitor.start_monitoring()


def stop_global_monitoring() -> Dict:
    """Detener monitoreo global y retornar resumen"""
    monitor = get_global_monitor()
    monitor.stop_monitoring()
    return monitor.get_performance_summary()