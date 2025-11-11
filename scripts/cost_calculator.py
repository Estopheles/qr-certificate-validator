#!/usr/bin/env python3
"""
Calculadora de costos independiente para análisis de diferentes cargas de trabajo
"""
import sys
import os
import json

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.cloud_cost_analyzer import CloudCostAnalyzer


def simulate_workload_scenarios():
    """Simular diferentes escenarios de carga de trabajo"""
    scenarios = {
        'light_workload': {
            'description': 'Carga ligera (10 PDFs, uso ocasional)',
            'performance_summary': {
                'monitoring_duration_seconds': 120,  # 2 minutos
                'process_metrics': {
                    'cpu_avg': 15.0,
                    'cpu_max': 35.0,
                    'memory_avg_mb': 150.0,
                    'memory_max_mb': 200.0,
                    'threads_max': 4
                }
            }
        },
        'medium_workload': {
            'description': 'Carga media (100 PDFs, uso regular)',
            'performance_summary': {
                'monitoring_duration_seconds': 1800,  # 30 minutos
                'process_metrics': {
                    'cpu_avg': 45.0,
                    'cpu_max': 75.0,
                    'memory_avg_mb': 400.0,
                    'memory_max_mb': 600.0,
                    'threads_max': 6
                }
            }
        },
        'heavy_workload': {
            'description': 'Carga pesada (500+ PDFs, uso intensivo)',
            'performance_summary': {
                'monitoring_duration_seconds': 7200,  # 2 horas
                'process_metrics': {
                    'cpu_avg': 70.0,
                    'cpu_max': 95.0,
                    'memory_avg_mb': 800.0,
                    'memory_max_mb': 1200.0,
                    'threads_max': 8
                }
            }
        }
    }
    
    return scenarios


def main():
    """Calculadora principal de costos"""
    print("="*80)
    print("💰 CALCULADORA DE COSTOS EN LA NUBE")
    print("="*80)
    
    analyzer = CloudCostAnalyzer()
    scenarios = simulate_workload_scenarios()
    
    for scenario_name, scenario_data in scenarios.items():
        print(f"\n{'='*60}")
        print(f"📊 ESCENARIO: {scenario_data['description'].upper()}")
        print(f"{'='*60}")
        
        # Analizar costos para este escenario
        analysis = analyzer.analyze_requirements(scenario_data['performance_summary'])
        analyzer.print_cost_analysis(analysis)
        
        # Guardar análisis detallado
        output_file = f"cost_analysis_{scenario_name}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n💾 Análisis guardado en: {output_file}")
    
    # Resumen comparativo
    print(f"\n{'='*80}")
    print("📈 RESUMEN COMPARATIVO DE COSTOS")
    print(f"{'='*80}")
    
    print("💡 RECOMENDACIONES GENERALES:")
    print("   • Para uso ocasional: AWS t3.small o GCP e2-small")
    print("   • Para uso regular: AWS t3.medium o Azure B2s")
    print("   • Para uso intensivo: AWS m5.large o Azure D2s_v3")
    print("   • Considera instancias spot para ahorrar 50-90%")
    print("   • Usa auto-scaling para cargas variables")
    
    print("\n💰 ESTRATEGIAS DE AHORRO:")
    print("   • Instancias reservadas: 30-60% descuento")
    print("   • Instancias spot: 50-90% descuento")
    print("   • Apagar instancias cuando no se usen")
    print("   • Usar contenedores (ECS/AKS/GKE) para mejor eficiencia")
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("   1. Ejecuta tu carga de trabajo real para obtener métricas precisas")
    print("   2. Compara precios actuales en las calculadoras oficiales:")
    print("      • AWS: https://calculator.aws")
    print("      • Azure: https://azure.microsoft.com/pricing/calculator/")
    print("      • GCP: https://cloud.google.com/products/calculator")
    print("   3. Considera factores adicionales: red, almacenamiento, transferencia")


if __name__ == "__main__":
    main()