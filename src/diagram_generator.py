#!/usr/bin/env python3
"""
Módulo para generar diagramas de transiciones de la Máquina de Turing.
Genera archivos en formato Mermaid (.md) y DOT/Graphviz (.dot).
"""

import os
import sys
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from loader import load_machine_config


def generate_mermaid_diagram(config: dict) -> str:
    """
    Genera un diagrama de estados en formato Mermaid.
    
    Args:
        config: Configuración de la máquina de Turing
    
    Returns:
        String con el diagrama Mermaid
    """
    lines = []
    lines.append("```mermaid")
    lines.append("stateDiagram-v2")
    
    # Estado inicial
    lines.append(f"    [*] --> {config['estado_inicial']}")
    
    # Estados de aceptación
    for state in config['estados_aceptacion']:
        lines.append(f"    {state} --> [*]")
    
    # Agrupar transiciones por (estado_origen, estado_destino)
    transitions_grouped = defaultdict(list)
    
    for state, trans_dict in config['transiciones'].items():
        for symbol, (next_state, write_symbol, direction) in trans_dict.items():
            # Usar caracteres especiales seguros para Mermaid
            symbol_display = symbol if symbol != '_' else 'β'
            write_display = write_symbol if write_symbol != '_' else 'β'
            
            label = f"{symbol_display}/{write_display},{direction}"
            transitions_grouped[(state, next_state)].append(label)
    
    # Generar transiciones
    for (src, dst), labels in transitions_grouped.items():
        # Combinar etiquetas si hay múltiples transiciones entre mismos estados
        combined_label = "\\n".join(labels) if len(labels) <= 3 else labels[0] + f"\\n... (+{len(labels)-1})"
        lines.append(f"    {src} --> {dst}: {combined_label}")
    
    lines.append("```")
    
    return '\n'.join(lines)


def generate_dot_diagram(config: dict) -> str:
    """
    Genera un diagrama de estados en formato DOT (Graphviz).
    
    Args:
        config: Configuración de la máquina de Turing
    
    Returns:
        String con el diagrama DOT
    """
    lines = []
    lines.append("digraph TuringMachine {")
    lines.append('    rankdir=LR;')
    lines.append('    size="14,10";')
    lines.append('    node [shape=circle, fontname="Helvetica", fontsize=10];')
    lines.append('    edge [fontname="Helvetica", fontsize=9];')
    lines.append('')
    
    # Punto de inicio
    lines.append('    start [shape=point, width=0];')
    lines.append(f'    start -> {config["estado_inicial"]};')
    lines.append('')
    
    # Estados de aceptación (doble círculo)
    accept_states = ' '.join(config['estados_aceptacion'])
    lines.append(f'    node [shape=doublecircle]; {accept_states};')
    lines.append('    node [shape=circle];')
    lines.append('')
    
    # Agrupar transiciones por (estado_origen, estado_destino)
    transitions_grouped = defaultdict(list)
    
    for state, trans_dict in config['transiciones'].items():
        for symbol, (next_state, write_symbol, direction) in trans_dict.items():
            # Usar caracteres especiales seguros
            symbol_display = symbol if symbol != '_' else 'β'
            write_display = write_symbol if write_symbol != '_' else 'β'
            
            label = f"{symbol_display}/{write_display},{direction}"
            transitions_grouped[(state, next_state)].append(label)
    
    # Generar transiciones
    for (src, dst), labels in sorted(transitions_grouped.items()):
        # Combinar etiquetas
        if len(labels) <= 4:
            combined_label = '\\n'.join(labels)
        else:
            combined_label = '\\n'.join(labels[:3]) + f'\\n... (+{len(labels)-3} más)'
        
        lines.append(f'    {src} -> {dst} [label="{combined_label}"];')
    
    lines.append('}')
    
    return '\n'.join(lines)


def generate_markdown_file(config: dict, mermaid_diagram: str) -> str:
    """
    Genera el contenido completo del archivo Markdown con el diagrama.
    
    Args:
        config: Configuración de la máquina de Turing
        mermaid_diagram: Diagrama Mermaid generado
    
    Returns:
        Contenido completo del archivo Markdown
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Contar transiciones
    total_transitions = sum(
        len(trans_dict) 
        for trans_dict in config['transiciones'].values()
    )
    
    content = f"""# Diagrama de Transiciones

## Máquina de Turing - {config.get('nombre', 'Sin nombre')}

{config.get('descripcion', '')}

> **Generado automáticamente:** {timestamp}

## Estadísticas

| Métrica | Valor |
|---------|-------|
| Estados | {len(config['estados'])} |
| Transiciones | {total_transitions} |
| Estado inicial | `{config['estado_inicial']}` |
| Estados de aceptación | {', '.join(f'`{s}`' for s in config['estados_aceptacion'])} |
| Alfabeto de cinta | {', '.join(f'`{s}`' for s in config['alfabeto_cinta'])} |

## Diagrama

{mermaid_diagram}

## Leyenda de Símbolos

| Símbolo | Significado |
|---------|-------------|
| β | Blanco (espacio vacío) |
"""
    
    # Usar leyenda del JSON si existe, sino usar valores por defecto
    if 'leyenda_simbolos' in config:
        for simbolo, significado in config['leyenda_simbolos'].items():
            content += f"| {simbolo} | {significado} |\n"
    else:
        # Valores por defecto para compatibilidad
        default_legend = {
            'C': 'Contador',
            'D': 'Contador usado',
            'A': 'F(i-1)',
            'B': 'F(i)',
            'X': 'Nuevo B',
            'Y': 'B marcado',
            'Z': 'A marcado'
        }
        for simbolo, significado in default_legend.items():
            content += f"| {simbolo} | {significado} |\n"

    content += """
## Lista de Estados

| Estado | Descripción |
|--------|-------------|
"""
    
    # Usar descripciones del JSON si existen, sino usar valores por defecto
    if 'descripcion_estados' in config:
        state_descriptions = config['descripcion_estados']
    else:
        # Descripciones por defecto para compatibilidad
        state_descriptions = {
            'q0': 'Estado inicial',
            'qN1': 'Leer primer símbolo de entrada',
            'qN2': 'Leer segundo símbolo de entrada',
            'qBase': 'Caso base (n=0 o n=1)',
            'qSetup': 'Configurar contador inicial',
            'qS2': 'Buscar posición para A',
            'qS3': 'Colocar B inicial',
            'qRew': 'Rebobinar al inicio de la cinta',
            'qChkC': 'Verificar contador',
            'qDecC': 'Decrementar contador',
            'qCpB': 'Copiar B (inicio)',
            'qCpB2': 'Copiar B (continuar)',
            'qCpB3': 'Copiar B (regresar)',
            'qCpA': 'Copiar A (inicio)',
            'qCpA2': 'Copiar A (continuar)',
            'qCpA3': 'Copiar A (regresar)',
            'qConv': 'Convertir marcadores',
            'qConv2': 'Finalizar conversión',
            'qOut': 'Limpiar cinta para salida',
            'qOut2': 'Escribir resultado final',
            'qaccept': 'Estado de aceptación'
        }
    
    for state in config['estados']:
        desc = state_descriptions.get(state, 'Estado auxiliar')
        content += f"| `{state}` | {desc} |\n"
    
    return content


def save_diagrams(config: dict, output_dir: str, verbose: bool = True) -> tuple:
    """
    Genera y guarda los archivos de diagrama.
    
    Args:
        config: Configuración de la máquina de Turing
        output_dir: Directorio donde guardar los archivos
        verbose: Si mostrar mensajes de progreso
    
    Returns:
        Tupla con las rutas de los archivos generados (md_path, dot_path)
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generar diagramas
    mermaid = generate_mermaid_diagram(config)
    dot = generate_dot_diagram(config)
    markdown = generate_markdown_file(config, mermaid)
    
    # Determinar nombre base del archivo
    machine_name = config.get('nombre', 'turing_machine')
    # Simplificar nombre para archivo
    base_name = 'fibonacci_diagrama'
    
    # Guardar archivos
    md_path = os.path.join(output_dir, f"{base_name}.md")
    dot_path = os.path.join(output_dir, f"{base_name}.dot")
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    with open(dot_path, 'w', encoding='utf-8') as f:
        f.write(dot)
    
    if verbose:
        print(f"Diagrama Mermaid guardado en: {md_path}")
        print(f"Diagrama DOT guardado en: {dot_path}")
    
    return md_path, dot_path


def generate_from_json(json_path: str, output_dir: str = None, 
                       verbose: bool = True) -> tuple:
    """
    Genera diagramas desde un archivo JSON de configuración.
    
    Args:
        json_path: Ruta al archivo JSON de configuración
        output_dir: Directorio de salida (por defecto: ../diagramas/)
        verbose: Si mostrar mensajes de progreso
    
    Returns:
        Tupla con las rutas de los archivos generados
    """
    config = load_machine_config(json_path)
    
    if output_dir is None:
        # Usar directorio diagramas/ relativo al proyecto
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(project_root, 'diagramas')
    
    return save_diagrams(config, output_dir, verbose)


def main():
    """Función principal para uso desde línea de comandos."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Genera diagramas de transiciones para Máquinas de Turing'
    )
    parser.add_argument(
        'config', 
        nargs='?',
        help='Archivo JSON de configuración de la máquina'
    )
    parser.add_argument(
        '-o', '--output',
        help='Directorio de salida para los diagramas'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Modo silencioso'
    )
    
    args = parser.parse_args()
    
    # Usar configuración por defecto si no se especifica
    if args.config is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        args.config = os.path.join(project_root, 'maquinas', 'fibonacci.json')
    
    try:
        md_path, dot_path = generate_from_json(
            args.config, 
            args.output, 
            verbose=not args.quiet
        )
        
        if not args.quiet:
            print("\n¡Diagramas generados exitosamente!")
            print(f"\nPara visualizar el diagrama DOT, ejecute:")
            print(f"  dot -Tpng {dot_path} -o {dot_path.replace('.dot', '.png')}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
