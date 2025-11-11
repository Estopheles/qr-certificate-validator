"""
Configuración central del proyecto QR Certificate Validator
"""
import os
import logging
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Fallback si python-dotenv no está disponible
    def load_dotenv():
        pass
    load_dotenv()

logger = logging.getLogger(__name__)

def get_env_var(key: str, default: str | None = None, required: bool = False) -> str:
    """Obtiene variable de entorno con validación"""
    value = os.getenv(key, default)
    
    if required and not value:
        raise ValueError(f"Variable de entorno requerida no encontrada: {key}")
    
    return value or ""

def validate_directory(path: str, create_if_missing: bool = False) -> str:
    """Valida y opcionalmente crea directorio"""
    # Prevenir path traversal
    path_obj = Path(path).resolve()
    project_root = Path(__file__).parent.resolve()
    
    # Verificar que el path esté dentro del proyecto
    try:
        path_obj.relative_to(project_root)
    except ValueError:
        raise ValueError(f"Path fuera del directorio del proyecto: {path}")
    
    path_obj = Path(path)
    
    if not path_obj.exists() and create_if_missing:
        try:
            path_obj.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directorio creado: {path}")
        except OSError as e:
            raise ValueError(f"No se pudo crear directorio {path}: {e}")
    
    if not path_obj.exists():
        raise ValueError(f"Directorio no existe: {path}")
    
    if not path_obj.is_dir():
        raise ValueError(f"Path no es directorio: {path}")
    
    return str(path_obj.absolute())

# Configuración con validación usando estructura del proyecto
PROJECT_ROOT = Path(__file__).parent

try:
    DEFAULT_INPUT_PATH = validate_directory(
        get_env_var('DEFAULT_INPUT_PATH', str(PROJECT_ROOT / 'data' / 'examples' / 'sample_certificates')),
        create_if_missing=True
    )
    DEFAULT_OUTPUT_PATH = validate_directory(
        get_env_var('DEFAULT_OUTPUT_PATH', str(PROJECT_ROOT / 'build' / 'reports')),
        create_if_missing=True
    )
except ValueError as e:
    logger.error(f"Error en configuración: {e}")
    raise

# Timeouts con validación
SELENIUM_TIMEOUT_SHORT = max(1, int(get_env_var('SELENIUM_TIMEOUT_SHORT', '8')))
SELENIUM_TIMEOUT_MEDIUM = max(SELENIUM_TIMEOUT_SHORT, int(get_env_var('SELENIUM_TIMEOUT_MEDIUM', '14')))
SELENIUM_TIMEOUT_LONG = max(SELENIUM_TIMEOUT_MEDIUM, int(get_env_var('SELENIUM_TIMEOUT_LONG', '18')))
SELENIUM_HEADLESS = get_env_var('SELENIUM_HEADLESS', 'true').lower() == 'true'

# Procesamiento con validación
MAX_WORKERS = max(1, min(8, int(get_env_var('MAX_WORKERS', '4'))))
ZOOM_LEVELS = [max(1, int(x)) for x in get_env_var('ZOOM_LEVELS', '2,3,4,5,6').split(',')]
DPI_LEVELS = [max(72, int(x)) for x in get_env_var('DPI_LEVELS', '150,200,300').split(',')]

# Logging
LOG_LEVEL = get_env_var('LOG_LEVEL', 'INFO')
LOG_FILE = get_env_var('LOG_FILE', 'process_log.txt')

# Constantes de procesamiento
CERTIFICATE_PRESENT_VALUE = get_env_var('CERTIFICATE_PRESENT_VALUE', 'SÍ')
