#!/usr/bin/env python3
"""
Simulador de Máquina de Turing Determinista de Una Cinta.
Proyecto 1 - Análisis y Diseño de Algoritmos
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loader import load_machine_config
from turing_machine import TuringMachine
from display import print_history, print_summary
from diagram_generator import generate_from_json


def get_input_string() -> str:
    """Solicita al usuario la cadena de entrada."""
    print("\n" + "="*60)
    print("ENTRADA")
    print("="*60)
    print("Ingrese n para calcular F(n) en notación unaria.")
    print("Ejemplos: '' (vacío) para F(0), '1' para F(1), '111' para F(3)")
    print("-"*60)
    
    while True:
        entrada = input("Entrada (n en unario): ").strip()
        
        # Validar que solo contenga '1's o esté vacía
        if all(c == '1' for c in entrada):
            return entrada
        
        print("Error: La entrada debe contener solo '1's o estar vacía.")


def run_simulation(machine: TuringMachine, input_str: str, 
                   show_steps: bool = True, max_steps: int = 100000):
    """
    Ejecuta la simulación de la máquina.
    
    Args:
        machine: Máquina de Turing configurada
        input_str: Cadena de entrada
        show_steps: Si mostrar los pasos de la simulación
        max_steps: Máximo de pasos permitidos
    
    Returns:
        Tupla (aceptado, pasos, resultado)
    """
    machine.reset(input_str)
    accepted = machine.run(max_steps)
    
    if show_steps:
        print("\n" + "="*60)
        print("CONFIGURACIONES DE LA SIMULACIÓN")
        print("="*60)
        
        # Decidir cuántos pasos mostrar
        total_steps = len(machine.history)
        if total_steps <= 50:
            print_history(machine.history, show_all=True)
        else:
            print_history(machine.history, max_display=30)
    
    print_summary(machine, input_str)
    
    return (accepted, machine.step_count, machine.get_result())


def to_unary(input_str: str) -> str:
    """Convierte entrada a unario si es número decimal."""
    if input_str.isdigit():
        return '1' * int(input_str)
    return input_str


def main():
    """Función principal del simulador."""
    # Ruta por defecto al archivo de configuración
    default_config = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "maquinas", "fibonacci.json"
    )
    
    # Permitir especificar configuración y entrada por argumentos
    # Uso: python simulator.py [config.json] [entrada] [verbose]
    config_path = sys.argv[1] if len(sys.argv) > 1 else default_config
    input_arg = sys.argv[2] if len(sys.argv) > 2 else None
    verbose = len(sys.argv) <= 3 or sys.argv[3] != "0"
    
    # Convertir entrada decimal a unario si aplica
    if input_arg is not None:
        input_arg = to_unary(input_arg)
    
    if verbose:
        print("\n" + "="*60)
        print("  SIMULADOR DE MÁQUINA DE TURING")
        print("  Cálculo de la Sucesión de Fibonacci")
        print("="*60)
        print(f"\nCargando configuración desde: {config_path}")
    
    try:
        config = load_machine_config(config_path)
        if verbose:
            print(f"Máquina cargada: {config.get('nombre', 'Sin nombre')}")
            print(f"Descripción: {config.get('descripcion', 'Sin descripción')}")
            
            # Generar diagramas automáticamente
            print("\nActualizando diagramas de transiciones...")
            generate_from_json(config_path, verbose=False)
            print("Diagramas actualizados en: diagramas/")
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        sys.exit(1)
    
    machine = TuringMachine(config)
    
    # Modo no interactivo si se proporcionó entrada por argumento
    if input_arg is not None:
        run_simulation(machine, input_arg, show_steps=verbose)
        return
    
    # Bucle principal (modo interactivo)
    while True:
        input_str = get_input_string()
        run_simulation(machine, input_str)
        
        print("\n¿Desea realizar otra simulación? (s/n): ", end="")
        if input().strip().lower() != 's':
            break
    
    print("\n¡Gracias por usar el simulador!\n")


if __name__ == "__main__":
    main()
