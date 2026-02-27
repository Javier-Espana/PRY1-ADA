"""
Módulo para visualizar las configuraciones de la Máquina de Turing.
"""


def format_configuration(config: dict, show_tape_ruler: bool = False) -> str:
    """
    Formatea una configuración para mostrarla.
    
    Args:
        config: Diccionario con la configuración (step, state, head, tape, offset)
        show_tape_ruler: Si mostrar números de posición
    
    Returns:
        String formateado de la configuración
    """
    step = config['step']
    state = config['state']
    head = config['head']
    tape = config['tape']
    offset = config['offset']
    
    # Posición relativa de la cabeza en el string de la cinta
    head_rel = head - offset
    
    # Crear indicador de cabeza
    head_indicator = ' ' * head_rel + '^'
    
    # Formatear salida
    lines = [
        f"Paso {step:4d} | Estado: {state:15s} | Cabeza: {head:3d}",
        f"         | Cinta: [{tape}]",
        f"         |        [{head_indicator}]"
    ]
    
    return '\n'.join(lines)


def print_history(history: list, max_display: int = None, 
                  show_all: bool = False, step_interval: int = 1):
    """
    Imprime el historial de configuraciones.
    
    Args:
        history: Lista de configuraciones
        max_display: Máximo de configuraciones a mostrar
        show_all: Si mostrar todas las configuraciones
        step_interval: Intervalo entre pasos mostrados
    """
    if not history:
        print("No hay historial de configuraciones.")
        return
    
    total = len(history)
    
    if show_all or (max_display and total <= max_display):
        configs_to_show = history[::step_interval]
    else:
        # Mostrar primeras y últimas
        n = max_display or 20
        half = n // 2
        configs_to_show = history[:half] + history[-half:]
        print(f"\n{'='*60}")
        print(f"Mostrando {n} de {total} configuraciones")
        print(f"{'='*60}\n")
    
    for i, config in enumerate(configs_to_show):
        print(format_configuration(config))
        if i < len(configs_to_show) - 1:
            print("-" * 50)
    
    print(f"\n{'='*60}")
    print(f"Total de pasos: {total - 1}")


def print_summary(machine, input_str: str):
    """
    Imprime un resumen de la ejecución.
    
    Args:
        machine: Instancia de TuringMachine
        input_str: Cadena de entrada
    """
    print(f"\n{'='*60}")
    print("RESUMEN DE EJECUCIÓN")
    print(f"{'='*60}")
    print(f"Entrada (n):     '{input_str}' ({len(input_str)} en unario)")
    print(f"Pasos totales:   {machine.step_count}")
    print(f"Estado final:    {machine.current_state}")
    print(f"Aceptado:        {'Sí' if machine.accepted else 'No'}")
    
    # Obtener resultado limpio
    clean_result = machine.get_clean_result()
    fib_value = len(clean_result)
    
    print(f"Resultado:       '{clean_result}' (F({len(input_str)}) = {fib_value})")
    print(f"{'='*60}\n")
