#!/usr/bin/env python3
"""
Script de verificación de seguridad
"""
import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Verifica vulnerabilidades en dependencias"""
    print("🔍 Verificando dependencias...")
    try:
        result = subprocess.run(['pip', 'list', '--outdated'], capture_output=True, text=True)
        if result.stdout:
            print("⚠️  Dependencias desactualizadas encontradas:")
            print(result.stdout)
        else:
            print("✅ Todas las dependencias están actualizadas")
    except Exception as e:
        print(f"❌ Error verificando dependencias: {e}")

def check_file_permissions():
    """Verifica permisos de archivos críticos"""
    print("\n🔍 Verificando permisos de archivos...")
    
    critical_files = [
        'config.py',
        '.env',
        'utils/security_validator.py'
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            mode = oct(stat.st_mode)[-3:]
            if mode in ['777', '666']:
                print(f"⚠️  {file_path} tiene permisos muy permisivos: {mode}")
            else:
                print(f"✅ {file_path} tiene permisos seguros: {mode}")
        else:
            print(f"❌ {file_path} no encontrado")

def check_security_imports():
    """Verifica que los módulos de seguridad estén importados"""
    print("\n🔍 Verificando importaciones de seguridad...")
    
    files_to_check = {
        'main.py': ['SecurityValidator', 'StructuredLogger'],
        'core/web_scraper.py': ['SecurityValidator'],
        'core/pdf_processor.py': ['SecurityValidator'],
        'utils/logger.py': ['SecurityValidator']
    }
    
    for file_path, required_imports in files_to_check.items():
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                for import_name in required_imports:
                    if import_name in content:
                        print(f"✅ {file_path} importa {import_name}")
                    else:
                        print(f"❌ {file_path} NO importa {import_name}")
        else:
            print(f"❌ {file_path} no encontrado")

def run_security_tests():
    """Ejecuta tests de seguridad"""
    print("\n🔍 Ejecutando tests de seguridad...")
    try:
        result = subprocess.run(['python', '-m', 'pytest', 'tests/test_security.py', '-v'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Todos los tests de seguridad pasaron")
        else:
            print("❌ Algunos tests de seguridad fallaron:")
            print(result.stdout)
            print(result.stderr)
    except Exception as e:
        print(f"❌ Error ejecutando tests: {e}")

def check_env_file():
    """Verifica configuración del archivo .env"""
    print("\n🔍 Verificando archivo .env...")
    
    if os.path.exists('.env'):
        print("✅ Archivo .env encontrado")
        # Verificar que no contenga credenciales hardcodeadas
        with open('.env', 'r') as f:
            content = f.read()
            if 'password' in content.lower() or 'secret' in content.lower():
                print("⚠️  Posibles credenciales encontradas en .env")
            else:
                print("✅ No se encontraron credenciales obvias en .env")
    else:
        print("⚠️  Archivo .env no encontrado, usando valores por defecto")

def main():
    """Función principal de verificación"""
    print("🔒 VERIFICACIÓN DE SEGURIDAD - QR Certificate Validator")
    print("=" * 60)
    
    check_dependencies()
    check_file_permissions()
    check_security_imports()
    check_env_file()
    run_security_tests()
    
    print("\n" + "=" * 60)
    print("✅ Verificación de seguridad completada")
    print("\n📋 Recomendaciones:")
    print("1. Ejecutar este script regularmente")
    print("2. Mantener dependencias actualizadas")
    print("3. Revisar logs de seguridad periódicamente")
    print("4. Validar configuraciones antes de producción")

if __name__ == "__main__":
    main()