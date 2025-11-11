"""
Manejador de estadísticas y resumen de procesamiento
"""
import pandas as pd
from typing import List, Dict


def print_processing_summary(all_results: List[Dict], pdf_count: int, total_time: float) -> None:
    """Imprime resumen final del procesamiento"""
    print("="*60)
    print("RESUMEN FINAL DEL PROCESAMIENTO")
    print("="*60)
    print(f"Tiempo total: {total_time:.2f} segundos")
    print(f"Total de PDFs procesados: {pdf_count}")
    print(f"Total de QR extraídos: {len(all_results)}")
    print(f"Promedio de QR por PDF: {len(all_results)/pdf_count:.2f}" if pdf_count > 0 else "Promedio: 0")
    
    if all_results:
        # Estadísticas de validación
        df_results = pd.DataFrame(all_results)
        validos = len(df_results[df_results['validacion_general'] == 'VALIDO'])
        parciales = len(df_results[df_results['validacion_general'] == 'PARCIALMENTE_VALIDO'])
        falsificaciones = len(df_results[df_results['validacion_general'] == 'POSIBLE_FALSIFICACION'])
        
        print(f"Certificados válidos: {validos}")
        print(f"Parcialmente válidos: {parciales}")
        print(f"Posibles falsificaciones: {falsificaciones}")
    
    print("="*60)