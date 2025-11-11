"""
Manejador de interfaz de línea de comandos
"""
import sys
import os
import glob
import logging
from datetime import datetime
from pathlib import Path
from typing import Tuple

import config

logger = logging.getLogger(__name__)


def parse_arguments() -> Tuple[str, str]:
    """Parsea argumentos de línea de comandos con fallback a valores por defecto"""
    try:
        if len(sys.argv) == 1:
            # Sin argumentos, usar valores por defecto
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(config.DEFAULT_OUTPUT_PATH, f"QR_Validado_Completo_{timestamp}.xlsx")
            return config.DEFAULT_INPUT_PATH, output_file
        elif len(sys.argv) == 2:
            # Solo input folder, output en build/reports
            input_folder = sys.argv[1]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'build', 'reports')
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"QR_Validado_Completo_{timestamp}.xlsx")
            return input_folder, output_file
        elif len(sys.argv) == 3:
            # Input y output especificados
            return sys.argv[1], sys.argv[2]
        else:
            print("Uso: python main.py [input_folder] [output_file]")
            sys.exit(1)
    except (AttributeError, IndexError) as e:
        logger.error(f"Error procesando argumentos: {e}")
        print("Error: Argumentos inválidos")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error inesperado en argumentos: {e}")
        print("Error: No se pudieron procesar los argumentos")
        sys.exit(1)


def validate_paths(input_folder: str, output_file: str) -> bool:
    """Valida que los paths sean válidos y seguros"""
    try:
        # Validar input folder existe
        if not os.path.exists(input_folder):
            logger.error(f"Carpeta de entrada no existe: {input_folder}")
            return False
        
        # Validar seguridad básica
        try:
            Path(input_folder).resolve()
            Path(output_file).resolve()
        except Exception as e:
            logger.error(f"Path inválido: {e}")
            return False
        
        # Verificar que hay PDFs
        pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
        if not pdf_files:
            logger.warning(f"No se encontraron archivos PDF en {input_folder}")
            return False
        
        # Crear directorio de salida si no existe
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                logger.info(f"Directorio de salida creado: {output_dir}")
            except (OSError, PermissionError) as e:
                logger.error(f"Error creando directorio de salida {output_dir}: {e}")
                return False
        
        return True
    
    except (OSError, PermissionError) as e:
        logger.error(f"Error de permisos validando paths: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado validando paths: {e}")
        return False


def cleanup_all_temp_files() -> None:
    """Limpia todos los archivos temporales generados por el proceso"""
    try:
        temp_files = glob.glob("temp_*.png")
        deleted_count = 0
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
                deleted_count += 1
            except Exception:
                pass
        
        if deleted_count > 0:
            print(f"Limpieza: {deleted_count} archivos temporales eliminados")
    except Exception:
        pass