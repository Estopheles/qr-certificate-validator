#!/usr/bin/env python3
"""
Analizador de costos en la nube basado en métricas de rendimiento
Ayuda a dimensionar correctamente instancias AWS/Azure/GCP
"""
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class CloudRecommendation:
    """Recomendación de instancia en la nube"""
    provider: str
    instance_type: str
    vcpus: int
    memory_gb: float
    cost_per_hour: float
    cost_per_month: float
    fit_score: int  # 1-100


class CloudCostAnalyzer:
    """Analizador de costos para diferentes proveedores de nube"""
    
    # Instancias AWS (us-east-1, precios aproximados 2024)
    AWS_INSTANCES = {
        't3.micro': {'vcpus': 2, 'memory_gb': 1, 'cost_hour': 0.0104},
        't3.small': {'vcpus': 2, 'memory_gb': 2, 'cost_hour': 0.0208},
        't3.medium': {'vcpus': 2, 'memory_gb': 4, 'cost_hour': 0.0416},
        't3.large': {'vcpus': 2, 'memory_gb': 8, 'cost_hour': 0.0832},
        't3.xlarge': {'vcpus': 4, 'memory_gb': 16, 'cost_hour': 0.1664},
        'm5.large': {'vcpus': 2, 'memory_gb': 8, 'cost_hour': 0.096},
        'm5.xlarge': {'vcpus': 4, 'memory_gb': 16, 'cost_hour': 0.192},
        'm5.2xlarge': {'vcpus': 8, 'memory_gb': 32, 'cost_hour': 0.384},
        'c5.large': {'vcpus': 2, 'memory_gb': 4, 'cost_hour': 0.085},
        'c5.xlarge': {'vcpus': 4, 'memory_gb': 8, 'cost_hour': 0.17},
        'r5.large': {'vcpus': 2, 'memory_gb': 16, 'cost_hour': 0.126},
        'r5.xlarge': {'vcpus': 4, 'memory_gb': 32, 'cost_hour': 0.252}
    }
    
    # Instancias Azure (precios aproximados 2024)
    AZURE_INSTANCES = {
        'B1s': {'vcpus': 1, 'memory_gb': 1, 'cost_hour': 0.0104},
        'B2s': {'vcpus': 2, 'memory_gb': 4, 'cost_hour': 0.0416},
        'D2s_v3': {'vcpus': 2, 'memory_gb': 8, 'cost_hour': 0.096},
        'D4s_v3': {'vcpus': 4, 'memory_gb': 16, 'cost_hour': 0.192},
        'F2s_v2': {'vcpus': 2, 'memory_gb': 4, 'cost_hour': 0.083},
        'F4s_v2': {'vcpus': 4, 'memory_gb': 8, 'cost_hour': 0.166}
    }
    
    # Instancias GCP (precios aproximados 2024)
    GCP_INSTANCES = {
        'e2-micro': {'vcpus': 1, 'memory_gb': 1, 'cost_hour': 0.0084},
        'e2-small': {'vcpus': 1, 'memory_gb': 2, 'cost_hour': 0.0168},
        'e2-medium': {'vcpus': 1, 'memory_gb': 4, 'cost_hour': 0.0336},
        'e2-standard-2': {'vcpus': 2, 'memory_gb': 8, 'cost_hour': 0.0672},
        'e2-standard-4': {'vcpus': 4, 'memory_gb': 16, 'cost_hour': 0.1344},
        'n1-standard-1': {'vcpus': 1, 'memory_gb': 3.75, 'cost_hour': 0.0475},
        'n1-standard-2': {'vcpus': 2, 'memory_gb': 7.5, 'cost_hour': 0.095},
        'n1-standard-4': {'vcpus': 4, 'memory_gb': 15, 'cost_hour': 0.19}
    }
    
    def analyze_requirements(self, performance_summary: Dict) -> Dict:
        """
        Analizar requerimientos basado en métricas de rendimiento
        
        Args:
            performance_summary: Resumen de rendimiento del monitor
            
        Returns:
            Análisis de requerimientos y recomendaciones
        """
        # Extraer métricas clave
        process_metrics = performance_summary.get('process_metrics', {})
        system_metrics = performance_summary.get('system_metrics', {})
        
        cpu_avg = process_metrics.get('cpu_avg', 0)
        cpu_max = process_metrics.get('cpu_max', 0)
        memory_avg_mb = process_metrics.get('memory_avg_mb', 0)
        memory_max_mb = process_metrics.get('memory_max_mb', 0)
        threads_max = process_metrics.get('threads_max', 1)
        duration = performance_summary.get('monitoring_duration_seconds', 0)
        
        # Calcular requerimientos mínimos (threads_max no es igual a vCPUs necesarios)
        required_memory_gb = max(memory_max_mb / 1024, 0.5)  # Mínimo 0.5GB
        # Los hilos no equivalen directamente a vCPUs - usar CPU usage como base
        cpu_based_vcpus = max(int(cpu_max / 50), 1)  # 1 vCPU por cada 50% de uso
        required_vcpus = min(cpu_based_vcpus, 4)  # Máximo 4 vCPUs para casos normales
        
        # Agregar margen de seguridad (50% más recursos)
        recommended_memory_gb = required_memory_gb * 1.5
        recommended_vcpus = max(required_vcpus, 2)  # Mínimo 2 vCPUs para estabilidad
        
        # Obtener recomendaciones por proveedor
        aws_recommendations = self._get_provider_recommendations('AWS', self.AWS_INSTANCES, recommended_vcpus, recommended_memory_gb, cpu_avg)
        azure_recommendations = self._get_provider_recommendations('Azure', self.AZURE_INSTANCES, recommended_vcpus, recommended_memory_gb, cpu_avg)
        gcp_recommendations = self._get_provider_recommendations('GCP', self.GCP_INSTANCES, recommended_vcpus, recommended_memory_gb, cpu_avg)
        
        # Calcular costos estimados
        cost_analysis = self._calculate_cost_scenarios(aws_recommendations + azure_recommendations + gcp_recommendations, duration)
        
        return {
            'requirements_analysis': {
                'measured_cpu_avg': cpu_avg,
                'measured_cpu_max': cpu_max,
                'measured_memory_avg_mb': memory_avg_mb,
                'measured_memory_max_mb': memory_max_mb,
                'measured_threads_max': threads_max,
                'execution_duration_seconds': duration,
                'required_memory_gb': round(required_memory_gb, 2),
                'required_vcpus': required_vcpus,
                'recommended_memory_gb': round(recommended_memory_gb, 2),
                'recommended_vcpus': recommended_vcpus
            },
            'cloud_recommendations': {
                'aws': aws_recommendations,
                'azure': azure_recommendations,
                'gcp': gcp_recommendations
            },
            'cost_analysis': cost_analysis
        }
    
    def _get_provider_recommendations(self, provider: str, instances: Dict, required_vcpus: int, required_memory_gb: float, cpu_usage: float) -> List[CloudRecommendation]:
        """Obtener recomendaciones para un proveedor específico"""
        recommendations = []
        
        for instance_type, specs in instances.items():
            # Verificar si la instancia cumple los requerimientos
            if specs['vcpus'] >= required_vcpus and specs['memory_gb'] >= required_memory_gb:
                # Calcular score de ajuste (0-100)
                cpu_fit = min(100, (specs['vcpus'] * 50) / max(cpu_usage, 1))  # Más vCPUs = mejor para CPU intensivo
                memory_fit = min(100, (specs['memory_gb'] * 100) / required_memory_gb)  # Memoria suficiente
                cost_efficiency = max(0, 100 - (specs['cost_hour'] * 1000))  # Penalizar costos altos
                
                fit_score = int((cpu_fit + memory_fit + cost_efficiency) / 3)
                
                recommendations.append(CloudRecommendation(
                    provider=provider,
                    instance_type=instance_type,
                    vcpus=specs['vcpus'],
                    memory_gb=specs['memory_gb'],
                    cost_per_hour=specs['cost_hour'],
                    cost_per_month=specs['cost_hour'] * 24 * 30,
                    fit_score=fit_score
                ))
        
        # Ordenar por score de ajuste (mejor primero)
        return sorted(recommendations, key=lambda x: x.fit_score, reverse=True)[:3]  # Top 3
    
    def _calculate_cost_scenarios(self, all_recommendations: List[CloudRecommendation], execution_duration: float) -> Dict:
        """Calcular diferentes escenarios de costo"""
        if not all_recommendations:
            return {'error': 'No hay recomendaciones disponibles'}
        
        # Encontrar la opción más barata y la mejor
        cheapest = min(all_recommendations, key=lambda x: x.cost_per_hour)
        best_fit = max(all_recommendations, key=lambda x: x.fit_score)
        
        # Calcular costos para diferentes patrones de uso
        scenarios = {
            'single_execution': {
                'description': 'Una ejecución (tiempo medido)',
                'duration_hours': execution_duration / 3600,
                'cheapest_cost': cheapest.cost_per_hour * (execution_duration / 3600),
                'best_fit_cost': best_fit.cost_per_hour * (execution_duration / 3600)
            },
            'daily_batch': {
                'description': 'Procesamiento diario (1 hora/día)',
                'duration_hours': 30,  # 1 hora x 30 días
                'cheapest_cost': cheapest.cost_per_hour * 30,
                'best_fit_cost': best_fit.cost_per_hour * 30
            },
            'weekly_batch': {
                'description': 'Procesamiento semanal (4 horas/semana)',
                'duration_hours': 16,  # 4 horas x 4 semanas
                'cheapest_cost': cheapest.cost_per_hour * 16,
                'best_fit_cost': best_fit.cost_per_hour * 16
            },
            'always_on': {
                'description': 'Instancia siempre activa (24/7)',
                'duration_hours': 720,  # 24 * 30
                'cheapest_cost': cheapest.cost_per_month,
                'best_fit_cost': best_fit.cost_per_month
            }
        }
        
        return {
            'cheapest_option': {
                'provider': cheapest.provider,
                'instance': cheapest.instance_type,
                'cost_per_hour': cheapest.cost_per_hour,
                'specs': f"{cheapest.vcpus} vCPUs, {cheapest.memory_gb}GB RAM"
            },
            'best_fit_option': {
                'provider': best_fit.provider,
                'instance': best_fit.instance_type,
                'cost_per_hour': best_fit.cost_per_hour,
                'fit_score': best_fit.fit_score,
                'specs': f"{best_fit.vcpus} vCPUs, {best_fit.memory_gb}GB RAM"
            },
            'cost_scenarios': scenarios
        }
    
    def print_cost_analysis(self, analysis: Dict) -> None:
        """Imprimir análisis de costos de forma legible"""
        print("\n" + "="*80)
        print("💰 ANÁLISIS DE COSTOS EN LA NUBE")
        print("="*80)
        
        req = analysis['requirements_analysis']
        print(f"📊 REQUERIMIENTOS MEDIDOS:")
        print(f"   CPU promedio: {req['measured_cpu_avg']:.1f}%")
        print(f"   RAM máxima: {req['measured_memory_max_mb']:.0f}MB")
        print(f"   Hilos máximos: {req['measured_threads_max']}")
        print(f"   Duración: {req['execution_duration_seconds']:.1f}s")
        
        print(f"\n🎯 REQUERIMIENTOS RECOMENDADOS:")
        print(f"   vCPUs: {req['recommended_vcpus']}")
        print(f"   RAM: {req['recommended_memory_gb']:.1f}GB")
        
        cost = analysis.get('cost_analysis', {})
        if cost and 'cheapest_option' in cost and 'best_fit_option' in cost:
            print(f"\n💡 OPCIONES RECOMENDADAS:")
            print(f"   💸 MÁS BARATA: {cost['cheapest_option']['provider']} {cost['cheapest_option']['instance']}")
            print(f"      ${cost['cheapest_option']['cost_per_hour']:.4f}/hora - {cost['cheapest_option']['specs']}")
            print(f"   🏆 MEJOR AJUSTE: {cost['best_fit_option']['provider']} {cost['best_fit_option']['instance']}")
            print(f"      ${cost['best_fit_option']['cost_per_hour']:.4f}/hora - {cost['best_fit_option']['specs']}")
            
            print(f"\n💰 ESCENARIOS DE COSTO MENSUAL:")
            for scenario_name, scenario in cost.get('cost_scenarios', {}).items():
                print(f"   {scenario['description']}:")
                print(f"      Más barata: ${scenario['cheapest_cost']:.2f}")
                print(f"      Mejor ajuste: ${scenario['best_fit_cost']:.2f}")
                print(f"      Ahorro: ${abs(scenario['best_fit_cost'] - scenario['cheapest_cost']):.2f}")
        else:
            print(f"\n⚠️  No se encontraron instancias que cumplan los requerimientos.")
            print(f"   Considera reducir la carga de trabajo o usar instancias personalizadas.")