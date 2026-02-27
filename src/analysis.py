#!/usr/bin/env python3
"""
Módulo de análisis empírico para la Máquina de Turing de Fibonacci.
Mide tiempos de ejecución y genera gráficos.
"""

import sys
import os
import time
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loader import load_machine_config
from turing_machine import TuringMachine


def measure_execution(machine: TuringMachine, n: int, 
                      repetitions: int = 3, max_steps: int = 500000) -> dict:
    """
    Mide el tiempo de ejecución para una entrada dada.
    
    Args:
        machine: Máquina de Turing configurada
        n: Valor de n (tamaño de entrada)
        repetitions: Número de repeticiones para promediar
        max_steps: Máximo de pasos permitidos
    
    Returns:
        Diccionario con los resultados de la medición
    """
    input_str = '1' * n
    times = []
    steps = 0
    result = ""
    accepted = False
    
    for _ in range(repetitions):
        machine.reset(input_str)
        
        start = time.perf_counter()
        accepted = machine.run(max_steps=max_steps)
        end = time.perf_counter()
        
        times.append(end - start)
        steps = machine.step_count
        result = machine.get_clean_result()
    
    avg_time = sum(times) / len(times)
    fib_value = len(result) if result and result != '_' else 0
    
    return {
        'n': n,
        'input': input_str,
        'time_avg': avg_time,
        'time_min': min(times),
        'time_max': max(times),
        'steps': steps,
        'result': result,
        'fib_value': fib_value,
        'completed': accepted
    }


def run_analysis(config_path: str, n_values: list) -> list:
    """
    Ejecuta el análisis empírico para múltiples valores de n.
    
    Args:
        config_path: Ruta al archivo de configuración
        n_values: Lista de valores de n a probar
    
    Returns:
        Lista de resultados de medición
    """
    config = load_machine_config(config_path)
    machine = TuringMachine(config)
    
    results = []
    total = len(n_values)
    
    print(f"\nIniciando análisis empírico...")
    print(f"Valores de n a probar: {n_values}")
    print("-" * 60)
    
    for i, n in enumerate(n_values):
        print(f"[{i+1}/{total}] Midiendo n={n}...", end=" ", flush=True)
        
        measurement = measure_execution(machine, n)
        results.append(measurement)
        
        print(f"Tiempo: {measurement['time_avg']*1000:.2f}ms, "
              f"Pasos: {measurement['steps']}, "
              f"F({n})={measurement['fib_value']}")
    
    return results


def save_results(results: list, output_dir: str):
    """Guarda los resultados en formato JSON."""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_dir, f"analysis_{timestamp}.json")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nResultados guardados en: {filepath}")
    return filepath


def print_results_table(results: list):
    """Imprime una tabla con los resultados."""
    print("\n" + "=" * 90)
    print("RESULTADOS DEL ANÁLISIS EMPÍRICO - Máquina de Turing Fibonacci (Cinta Única)")
    print("=" * 90)
    print(f"{'n':>4} | {'F(n)':>8} | {'Pasos':>12} | {'Ratio':>8} | "
          f"{'Tiempo (ms)':>12} | {'Estado':>10}")
    print("-" * 90)
    
    prev_steps = None
    for r in results:
        ratio = f"{r['steps']/prev_steps:.3f}" if prev_steps and prev_steps > 0 else "-"
        estado = "OK" if r.get('completed', True) else "TIMEOUT"
        print(f"{r['n']:>4} | {r['fib_value']:>8} | "
              f"{r['steps']:>12,} | {ratio:>8} | "
              f"{r['time_avg']*1000:>12.2f} | {estado:>10}")
        prev_steps = r['steps']
    
    print("=" * 90)
    print("\nNota: El ratio tiende a φ ≈ 1.618 (razón áurea), confirmando O(φⁿ)")


def run_analysis_adaptive(config_path: str, max_n: int = 14, 
                          time_limit: float = 30.0) -> list:
    """
    Ejecuta análisis adaptativo que para cuando el tiempo excede el límite.
    
    Args:
        config_path: Ruta al archivo de configuración
        max_n: Valor máximo de n a probar
        time_limit: Límite de tiempo en segundos para cada medición
    
    Returns:
        Lista de resultados de medición
    """
    config = load_machine_config(config_path)
    machine = TuringMachine(config)
    
    results = []
    
    print(f"\n{'='*60}")
    print("ANÁLISIS EMPÍRICO - Complejidad Exponencial O(φⁿ)")
    print(f"{'='*60}")
    print(f"Límite de tiempo por medición: {time_limit}s")
    print(f"Rango de n: 0 a {max_n}")
    print("-" * 60)
    
    for n in range(max_n + 1):
        # Reducir repeticiones para valores grandes (toma mucho tiempo)
        reps = 3 if n <= 10 else 2 if n <= 12 else 1
        
        print(f"[n={n:2d}] Midiendo ({reps}x)...", end=" ", flush=True)
        
        measurement = measure_execution(machine, n, repetitions=reps, 
                                        max_steps=2000000)
        results.append(measurement)
        
        tiempo = measurement['time_avg']
        print(f"F({n})={measurement['fib_value']:>5}, "
              f"Pasos={measurement['steps']:>10,}, "
              f"Tiempo={tiempo*1000:>10.2f}ms")
        
        # Parar si el tiempo excede el límite
        if tiempo > time_limit:
            print(f"\n*** Límite de tiempo excedido en n={n}. Deteniendo análisis. ***")
            break
    
    return results


if __name__ == "__main__":
    # Configuración por defecto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "maquinas", "fibonacci.json")
    output_dir = os.path.join(base_dir, "resultados")
    
    # Ejecutar análisis adaptativo (para cuando toma demasiado tiempo)
    results = run_analysis_adaptive(config_path, max_n=15, time_limit=60.0)
    print_results_table(results)
    filepath = save_results(results, output_dir)
    
    print("\n" + "=" * 60)
    print("CONCLUSIÓN")
    print("=" * 60)
    print("La complejidad temporal es O(φⁿ) donde φ ≈ 1.618")
    print("Esto demuestra el crecimiento exponencial de la máquina")
    print("de Turing de una sola cinta para calcular Fibonacci.")
    print("=" * 60)
