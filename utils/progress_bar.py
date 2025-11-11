"""
Utilidades para mostrar progreso en la consola
"""
import time
from tqdm import tqdm


def show_progress_bar(
    duration: int, 
    description: str = "Esperando", 
    attempt: int = 1, 
    total_attempts: int = 3
) -> None:
    """
    Muestra una barra de progreso durante la espera con información de intentos
    
    Args:
        duration: Segundos a esperar
        description: Descripción de la operación
        attempt: Número de intento actual
        total_attempts: Total de intentos
    """
    full_desc = f"Intento {attempt}/{total_attempts} ({duration}s) - {description}"
    bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt}s [{elapsed}<{remaining}]"
    
    with tqdm(
        total=duration, 
        desc=full_desc, 
        unit="s", 
        ncols=100, 
        bar_format=bar_format
    ) as pbar:
        for _ in range(duration):
            time.sleep(1)
            pbar.update(1)
