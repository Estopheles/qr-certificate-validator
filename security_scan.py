#!/usr/bin/env python3
"""
Escáner de seguridad independiente para archivos PDF
Uso: python security_scan.py <archivo_o_directorio>
"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime

from utils.pdf_security_analyzer import PDFSecurityAnalyzer


def scan_single_file(pdf_path: str) -> None:
    """Escanea un solo archivo PDF"""
    analyzer = PDFSecurityAnalyzer()
    result = analyzer.analyze_pdf_security(pdf_path)
    
    print(f"\n{'='*60}")
    print(f"ANÁLISIS DE SEGURIDAD: {Path(pdf_path).name}")
    print(f"{'='*60}")
    
    if 'error' in result:
        print(f"❌ ERROR: {result['error']}")
        return
    
    # Información del archivo
    file_info = result['file_info']
    print(f"📁 Archivo: {file_info['filename']}")
    print(f"📏 Tamaño: {file_info['size_mb']} MB")
    print(f"🔐 SHA256: {file_info['sha256'][:16]}...")
    
    # Análisis de riesgo
    risk = result['risk_assessment']
    risk_level = risk['overall_risk']
    
    # Emoji según riesgo
    risk_emoji = {
        'SAFE': '✅',
        'LOW': '🟡', 
        'MEDIUM': '🟠',
        'HIGH': '🔴',
        'CRITICAL': '💀'
    }.get(risk_level, '❓')
    
    print(f"\n{risk_emoji} NIVEL DE RIESGO: {risk_level}")
    print(f"📊 Puntuación: {risk['risk_score']}")
    print(f"💡 Recomendación: {risk['recommendation']}")
    
    # Amenazas encontradas
    if risk['threats']:
        print(f"\n⚠️  AMENAZAS DETECTADAS ({len(risk['threats'])}):")
        for i, threat in enumerate(risk['threats'], 1):
            print(f"  {i}. {threat}")
    else:
        print(f"\n✅ No se detectaron amenazas")
    
    # Elementos de riesgo
    risky_elements = result['raw_analysis'].get('risky_elements_found', {})
    if risky_elements:
        print(f"\n🚨 ELEMENTOS DE RIESGO:")
        for element, info in risky_elements.items():
            print(f"  • {element}: {info['count']} veces (Riesgo: {info['risk_level']})")
    
    # Referencias externas
    external_refs = result['raw_analysis'].get('external_references', [])
    if external_refs:
        print(f"\n🌐 REFERENCIAS EXTERNAS ({len(external_refs)}):")
        for ref in external_refs[:5]:  # Mostrar máximo 5
            print(f"  • {ref}")
        if len(external_refs) > 5:
            print(f"  ... y {len(external_refs) - 5} más")


def scan_directory(directory: str) -> None:
    """Escanea todos los PDFs en un directorio"""
    pdf_files = list(Path(directory).glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No se encontraron archivos PDF en {directory}")
        return
    
    print(f"🔍 Escaneando {len(pdf_files)} archivos PDF...")
    
    analyzer = PDFSecurityAnalyzer()
    results = []
    
    for pdf_file in pdf_files:
        result = analyzer.analyze_pdf_security(str(pdf_file))
        results.append({
            'file': pdf_file.name,
            'result': result
        })
    
    # Resumen por nivel de riesgo
    risk_summary = {'SAFE': 0, 'LOW': 0, 'MEDIUM': 0, 'HIGH': 0, 'CRITICAL': 0, 'ERROR': 0}
    
    print(f"\n{'='*60}")
    print(f"RESUMEN DE SEGURIDAD")
    print(f"{'='*60}")
    
    for item in results:
        result = item['result']
        if 'error' in result:
            risk_level = 'ERROR'
        else:
            risk_level = result['risk_assessment']['overall_risk']
        
        risk_summary[risk_level] += 1
        
        # Mostrar línea de resumen
        risk_emoji = {
            'SAFE': '✅', 'LOW': '🟡', 'MEDIUM': '🟠', 
            'HIGH': '🔴', 'CRITICAL': '💀', 'ERROR': '❌'
        }.get(risk_level, '❓')
        
        print(f"{risk_emoji} {item['file']:<40} {risk_level}")
    
    # Estadísticas finales
    print(f"\n📊 ESTADÍSTICAS:")
    total = len(results)
    for level, count in risk_summary.items():
        if count > 0:
            percentage = (count / total) * 100
            print(f"  {level}: {count} archivos ({percentage:.1f}%)")
    
    # Archivos que requieren atención
    dangerous = risk_summary['HIGH'] + risk_summary['CRITICAL']
    if dangerous > 0:
        print(f"\n⚠️  {dangerous} archivos requieren atención inmediata")
    
    # Guardar reporte detallado
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"security_report_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Reporte detallado guardado en: {report_file}")


def main():
    """Función principal del escáner"""
    if len(sys.argv) != 2:
        print("Uso: python security_scan.py <archivo_o_directorio>")
        print("\nEjemplos:")
        print("  python security_scan.py certificado.pdf")
        print("  python security_scan.py /ruta/a/pdfs/")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if not os.path.exists(target):
        print(f"❌ Error: {target} no existe")
        sys.exit(1)
    
    print(f"🔍 Iniciando análisis de seguridad PDF...")
    print(f"📂 Objetivo: {target}")
    
    if os.path.isfile(target):
        if target.lower().endswith('.pdf'):
            scan_single_file(target)
        else:
            print(f"❌ Error: {target} no es un archivo PDF")
    elif os.path.isdir(target):
        scan_directory(target)
    else:
        print(f"❌ Error: {target} no es un archivo ni directorio válido")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Análisis interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        raise