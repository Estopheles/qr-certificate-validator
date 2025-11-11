#!/usr/bin/env python3
"""
QR Certificate Validator - Punto de entrada principal
"""
import os
import logging
import time

from utils.logger import ProcessLogger
from utils.structured_logger import StructuredLogger
from utils.cli_handler import parse_arguments, validate_paths, cleanup_all_temp_files
from utils.stats_handler import print_processing_summary
from utils.resource_monitor import start_global_monitoring, stop_global_monitoring, get_global_monitor
from utils.cloud_cost_analyzer import CloudCostAnalyzer
from core.pdf_processor import process_single_pdf_with_validation
from output.report_generator import save_results_enhanced_with_validation

# Configurar logging (solo errores críticos como en original)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
structured_logger = StructuredLogger(__name__)


def main():
    """Función principal que ejecuta el proceso completo"""
    print("="*60)
    print("EXTRACCIÓN Y VALIDACIÓN DE QR DESDE PDFs")
    print("="*60)
    
    # INICIAR MONITOREO DE RECURSOS
    start_global_monitoring(interval=0.5)
    monitor = get_global_monitor()
    print("🔍 Monitor de recursos iniciado")
    
    # Parsear argumentos
    folder_path, output_file = parse_arguments()
    
    print(f"Configuración:")
    print(f"  Input: {folder_path}")
    print(f"  Output: {output_file}")
    
    # Validar paths
    if not validate_paths(folder_path, output_file):
        return
    
    # Inicializar logger
    process_log = ProcessLogger()
    
    # Obtener lista de PDFs
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    print(f"Encontrados {len(pdf_files)} archivos PDF")
    
    # Procesar PDFs
    start_time = time.time()
    all_results = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\nProcesando archivo {i}/{len(pdf_files)}: {pdf_file}")
        
        try:
            results = process_single_pdf_with_validation(pdf_file, folder_path, process_log)
            all_results.extend(results)
            structured_logger.log_processing_event(pdf_file, "SUCCESS", {"qr_count": len(results)})
            
            # Pausa entre PDFs para estabilidad
            if i < len(pdf_files):
                time.sleep(2)
        except FileNotFoundError as e:
            logger.error(f"Archivo no encontrado {pdf_file}: {e}")
            structured_logger.log_processing_event(pdf_file, "FILE_NOT_FOUND", {"error": str(e)})
            continue
        except PermissionError as e:
            logger.error(f"Sin permisos para {pdf_file}: {e}")
            structured_logger.log_processing_event(pdf_file, "PERMISSION_ERROR", {"error": str(e)})
            continue
        except ValueError as e:
            logger.error(f"Valor inválido en {pdf_file}: {e}")
            structured_logger.log_processing_event(pdf_file, "VALUE_ERROR", {"error": str(e)})
            continue
        except Exception as e:
            logger.error(f"Error inesperado procesando {pdf_file}: {e}")
            structured_logger.log_processing_event(pdf_file, "UNEXPECTED_ERROR", {"error": str(e), "type": type(e).__name__})
            if isinstance(e, (MemoryError, KeyboardInterrupt)):
                raise
            continue
    
    total_time = time.time() - start_time
    
    # Guardar resultados
    if all_results:
        save_results_enhanced_with_validation(all_results, output_file)
        print(f"\nResultados guardados en: {output_file}")
        
        # Exportar JSON de resultados
        import json
        json_file = output_file.replace('.xlsx', '_results.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
        print(f"📄 Resultados JSON: {json_file}")
        
        print_processing_summary(all_results, len(pdf_files), total_time)
    else:
        print("\nNo se encontraron datos para guardar.")
    
    # DETENER MONITOREO Y MOSTRAR RESUMEN
    performance_summary = stop_global_monitoring()
    print("\n" + "="*60)
    print("📊 RESUMEN DE RENDIMIENTO")
    print("="*60)
    print(f"⏱️  Duración total: {performance_summary.get('monitoring_duration_seconds', 0):.2f}s")
    print(f"🖥️  CPU promedio: {performance_summary.get('system_metrics', {}).get('cpu_avg', 0):.1f}%")
    print(f"💾 RAM promedio: {performance_summary.get('system_metrics', {}).get('memory_avg', 0):.1f}%")
    print(f"🔧 Proceso CPU: {performance_summary.get('process_metrics', {}).get('cpu_avg', 0):.1f}%")
    print(f"📈 Proceso RAM: {performance_summary.get('process_metrics', {}).get('memory_avg_mb', 0):.1f}MB")
    print(f"🧵 Hilos máx: {performance_summary.get('process_metrics', {}).get('threads_max', 0)}")
    
    # ANÁLISIS DE COSTOS EN LA NUBE
    cost_analyzer = CloudCostAnalyzer()
    cost_analysis = cost_analyzer.analyze_requirements(performance_summary)
    cost_analyzer.print_cost_analysis(cost_analysis)
    
    # Exportar métricas detalladas
    metrics_file = output_file.replace('.xlsx', '_metrics.json')
    monitor.export_detailed_metrics(metrics_file)
    print(f"📋 Métricas detalladas: {metrics_file}")
    
    # Exportar análisis de costos
    import json
    cost_file = output_file.replace('.xlsx', '_cloud_costs.json')
    with open(cost_file, 'w', encoding='utf-8') as f:
        json.dump(cost_analysis, f, indent=2, ensure_ascii=False, default=str)
    print(f"💰 Análisis de costos: {cost_file}")
    
    # Limpieza
    cleanup_all_temp_files()
    
    print("\nPROCESO COMPLETADO")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProceso interrumpido por el usuario")
        # Detener monitoreo antes de limpiar
        try:
            stop_global_monitoring()
        except (RuntimeError, OSError):
            pass
        cleanup_all_temp_files()
        import sys
        sys.exit(1)  # Exit code para interrupción
    except (RuntimeError, OSError, ImportError) as e:
        print(f"\nError crítico: {e}")
        logger.error(f"Error crítico en main: {e}")
        # Detener monitoreo antes de limpiar
        try:
            stop_global_monitoring()
        except (RuntimeError, OSError):
            pass
        cleanup_all_temp_files()
        raise
    except SystemExit:
        # Permitir salida normal del sistema
        raise
