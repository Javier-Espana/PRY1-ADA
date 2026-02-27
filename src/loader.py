"""
Módulo para cargar configuraciones de Máquinas de Turing desde archivos.
"""

import json
from pathlib import Path


def load_machine_config(filepath: str) -> dict:
    """
    Carga la configuración de una Máquina de Turing desde un archivo JSON.
    
    Args:
        filepath: Ruta al archivo de configuración
    
    Returns:
        Diccionario con la configuración de la máquina
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        json.JSONDecodeError: Si el archivo no es JSON válido
        ValueError: Si faltan campos requeridos
    """
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {filepath}")
    
    with open(path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    validate_config(config)
    return config


def validate_config(config: dict):
    """
    Valida que la configuración tenga todos los campos requeridos.
    
    Args:
        config: Diccionario de configuración
    
    Raises:
        ValueError: Si falta algún campo requerido
    """
    required_fields = [
        'estados',
        'estado_inicial', 
        'estados_aceptacion',
        'alfabeto_cinta',
        'simbolo_blanco',
        'transiciones'
    ]
    
    missing = [field for field in required_fields if field not in config]
    
    if missing:
        raise ValueError(f"Campos requeridos faltantes: {', '.join(missing)}")
    
    # Validar que el estado inicial esté en los estados
    if config['estado_inicial'] not in config['estados']:
        raise ValueError("El estado inicial no está en la lista de estados")
    
    # Validar estados de aceptación
    for state in config['estados_aceptacion']:
        if state not in config['estados']:
            raise ValueError(f"Estado de aceptación '{state}' no está en estados")


def get_transition(config: dict, state: str, symbol: str) -> tuple:
    """
    Obtiene la transición para un estado y símbolo dados.
    
    Args:
        config: Configuración de la máquina
        state: Estado actual
        symbol: Símbolo leído
    
    Returns:
        Tupla (nuevo_estado, simbolo_escribir, direccion) o None si no existe
    """
    transitions = config.get('transiciones', {})
    
    if state in transitions and symbol in transitions[state]:
        trans = transitions[state][symbol]
        return (trans[0], trans[1], trans[2])
    
    return None
