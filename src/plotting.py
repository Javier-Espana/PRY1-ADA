#!/usr/bin/env python3
"""
Módulo para generar gráficos del análisis empírico.
Genera diagrama de dispersión con regresión exponencial y polinomial.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import curve_fit


def load_analysis_results(filepath: str) -> list:
    """Carga los resultados del análisis desde un archivo JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def exponential_func(x, a, b):
    """Función exponencial: a * b^x"""
    return a * np.power(b, x)


def plot_exponential_analysis(results: list, output_dir: str, 
                               metric: str = 'steps'):
    """
    Genera diagrama de dispersión con regresión exponencial.
    
    Args:
        results: Lista de resultados del análisis
        output_dir: Directorio para guardar los gráficos
        metric: 'steps' para pasos o 'time' para tiempo
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Extraer datos (filtrar n=0 para evitar problemas)
    n_values = np.array([r['n'] for r in results if r['n'] > 0])
    
    if metric == 'steps':
        y_values = np.array([r['steps'] for r in results if r['n'] > 0])
        y_label = 'Número de Pasos'
        title = 'Pasos de Ejecución vs Tamaño de Entrada\n(Complejidad Exponencial)'
    else:
        y_values = np.array([r['time_avg'] * 1000 for r in results if r['n'] > 0])
        y_label = 'Tiempo (ms)'
        title = 'Tiempo de Ejecución vs Tamaño de Entrada\n(Complejidad Exponencial)'
    
    # Crear figura con dos subplots: escala lineal y logarítmica
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # === Gráfico 1: Escala lineal ===
    ax1.scatter(n_values, y_values, color='blue', s=100, 
                label='Datos observados', zorder=5, edgecolors='black')
    
    # Intentar ajuste exponencial
    try:
        # Usar valores iniciales basados en φ (razón áurea)
        popt, pcov = curve_fit(exponential_func, n_values, y_values, 
                               p0=[1, 1.618], maxfev=10000)
        a, b = popt
        
        # Línea suave para la regresión exponencial
        x_smooth = np.linspace(n_values.min(), n_values.max(), 100)
        y_smooth = exponential_func(x_smooth, a, b)
        
        ax1.plot(x_smooth, y_smooth, color='red', linewidth=2,
                 label=f'Regresión: {a:.2f} × {b:.3f}ⁿ')
        
        # Calcular R²
        y_pred = exponential_func(n_values, a, b)
        ss_res = np.sum((y_values - y_pred) ** 2)
        ss_tot = np.sum((y_values - np.mean(y_values)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        # Anotación con información
        info_text = f'f(n) = {a:.2f} × {b:.3f}ⁿ\nR² = {r2:.4f}\nBase ≈ φ = 1.618'
        ax1.text(0.05, 0.95, info_text, transform=ax1.transAxes,
                 fontsize=10, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        exp_base = b
    except Exception as e:
        print(f"Advertencia: No se pudo ajustar exponencial: {e}")
        exp_base = None
    
    ax1.set_xlabel('n (Tamaño de entrada)', fontsize=12)
    ax1.set_ylabel(y_label, fontsize=12)
    ax1.set_title(title, fontsize=12)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    
    # === Gráfico 2: Escala logarítmica ===
    ax2.scatter(n_values, y_values, color='blue', s=100, 
                label='Datos observados', zorder=5, edgecolors='black')
    ax2.set_yscale('log')
    
    # En escala log, una exponencial debería verse como línea recta
    if exp_base:
        ax2.plot(x_smooth, y_smooth, color='red', linewidth=2,
                 label=f'O(φⁿ) donde φ≈{exp_base:.3f}')
    
    ax2.set_xlabel('n (Tamaño de entrada)', fontsize=12)
    ax2.set_ylabel(f'{y_label} (escala log)', fontsize=12)
    ax2.set_title('Escala Logarítmica\n(Línea recta = crecimiento exponencial)', fontsize=12)
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    
    # Guardar gráfico
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"grafico_{metric}_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfico guardado en: {filepath}")
    return filepath, exp_base


def plot_ratio_analysis(results: list, output_dir: str):
    """
    Genera gráfico del ratio de crecimiento entre pasos consecutivos.
    Debería converger a φ ≈ 1.618 para crecimiento O(φⁿ).
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Calcular ratios
    n_values = []
    ratios = []
    prev_steps = None
    
    for r in results:
        if prev_steps and prev_steps > 0 and r['n'] > 1:
            ratio = r['steps'] / prev_steps
            n_values.append(r['n'])
            ratios.append(ratio)
        prev_steps = r['steps']
    
    if len(ratios) < 2:
        print("No hay suficientes datos para el análisis de ratio")
        return None, None
    
    n_values = np.array(n_values)
    ratios = np.array(ratios)
    
    # Crear gráfico
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.bar(n_values, ratios, color='steelblue', edgecolor='black', alpha=0.7)
    ax.axhline(y=1.618, color='red', linestyle='--', linewidth=2, 
               label='φ ≈ 1.618 (razón áurea)')
    
    ax.set_xlabel('n', fontsize=12)
    ax.set_ylabel('Ratio: Pasos(n) / Pasos(n-1)', fontsize=12)
    ax.set_title('Ratio de Crecimiento - Convergencia a φ\n(Confirma complejidad O(φⁿ))', fontsize=12)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Anotación con promedio
    avg_ratio = np.mean(ratios[-5:]) if len(ratios) >= 5 else np.mean(ratios)
    ax.text(0.95, 0.05, f'Promedio últimos valores: {avg_ratio:.3f}', 
            transform=ax.transAxes, fontsize=10, horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Guardar
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"grafico_ratio_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfico de ratio guardado en: {filepath}")
    return filepath, avg_ratio


if __name__ == "__main__":
    import sys
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, "resultados")
    
    # Buscar el archivo de resultados más reciente
    if len(sys.argv) > 1:
        results_file = sys.argv[1]
    else:
        json_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
        if not json_files:
            print("No se encontraron archivos de resultados.")
            print("Ejecute primero: python analysis.py")
            sys.exit(1)
        
        json_files.sort(reverse=True)
        results_file = os.path.join(results_dir, json_files[0])
    
    print(f"Cargando resultados desde: {results_file}")
    results = load_analysis_results(results_file)
    
    print("\n" + "="*60)
    print("GENERACIÓN DE GRÁFICOS - Análisis Exponencial")
    print("="*60)
    
    # Generar gráficos de pasos y tiempo con ajuste exponencial
    plot_exponential_analysis(results, results_dir, metric='steps')
    plot_exponential_analysis(results, results_dir, metric='time')
    
    # Generar gráfico de ratio (convergencia a φ)
    plot_ratio_analysis(results, results_dir)
    
    print("\n" + "="*60)
    print("Gráficos generados exitosamente.")
    print("="*60)
