# Proyecto 1: Máquina de Turing - Sucesión de Fibonacci

**Curso:** Análisis y Diseño de Algoritmos  
**Fecha de entrega:** Febrero 2026

## Descripción

Este proyecto implementa un **simulador de Máquina de Turing determinista de una cinta** que calcula la sucesión de Fibonacci. El objetivo es evaluar la comprensión de la notación O en el tiempo de ejecución de algoritmos.

La máquina utiliza una única cinta para almacenar el contador de iteraciones y todos los términos de la secuencia Fibonacci calculados, lo que resulta en una **complejidad temporal exponencial** O(φⁿ).

**Características:**
- Verificación de paridad usando estados alternantes (simula memoria cache)
- Secuencia calculada: 1, 1, 2, 3, 5, 8, 13... (omite F(0)=0 por convención)
- 24 estados y 58 transiciones

## Estructura del Proyecto

```
Proyecto1-ADA/
├── README.md                 # Este archivo
├── documentacion/
│   ├── CONVENCIONES.md       # Convenciones para representación de números
│   ├── DIAGRAMA_MT.md        # Diagrama de la Máquina de Turing
│   └── ANALISIS_COMPLEJIDAD.md # Análisis formal de notación O
├── diagramas/
│   ├── fibonacci_diagrama.md  # Diagrama Mermaid de transiciones
│   └── fibonacci_diagrama.dot # Diagrama Graphviz
├── maquinas/
│   └── fibonacci.json        # Configuración de la MT para Fibonacci
├── resultados/
│   ├── analysis_*.json       # Datos del análisis empírico
│   ├── grafico_steps_*.png   # Diagrama de dispersión (pasos)
│   └── grafico_time_*.png    # Diagrama de dispersión (tiempo)
└── src/
    ├── simulator.py          # Programa principal del simulador
    ├── turing_machine.py     # Implementación de la MT
    ├── tape.py               # Implementación de la cinta
    ├── loader.py             # Carga de configuraciones
    ├── display.py            # Visualización de configuraciones
    ├── diagram_generator.py  # Generador de diagramas
    ├── analysis.py           # Análisis empírico
    └── plotting.py           # Generación de gráficos
```

## Requisitos

- Python 3.8+
- NumPy
- Matplotlib

```bash
pip install numpy matplotlib
```

## Uso

### Simulador Interactivo

```bash
cd src
python simulator.py
```

El programa solicitará la entrada en notación unaria (ejemplo: `111` para n=3).

### Ejecución con Argumentos

```bash
# Usando notación unaria
python src/simulator.py maquinas/fibonacci.json 11111

# Usando número decimal (se convierte automáticamente)
python src/simulator.py maquinas/fibonacci.json 5
```

### Análisis Empírico

```bash
# Ejecutar mediciones
python src/analysis.py

# Generar gráficos
python src/plotting.py
```

## Convenciones

### Representación de Números

Los enteros no negativos se representan en **notación unaria**:
- `0` → (vacío)
- `1` → `1`
- `2` → `11`
- `3` → `111`
- `n` → `111...1` (n unos)

### Alfabeto de la Cinta

| Símbolo | Significado |
|---------|-------------|
| `1` | Dígito unario |
| `_` | Blanco (espacio vacío) |
| `#` | Marcador de inicio de cinta |
| `.` | Separador zona de contador y trabajo |
| `;` | Separador entre términos Fibonacci |
| `x` | Contador usado/procesado |
| `y`, `z` | Marcadores temporales para copia |

### Estructura de la Cinta

Durante la ejecución, la cinta mantiene el formato:
```
#[contador].[término1];[término2];...;[términoN];
```

### Entrada y Salida

- **Entrada:** `n` en unario para calcular F(n)
- **Salida:** F(n) en unario (último término de la secuencia)

| Entrada | n | F(n) | Pasos | Salida |
|---------|---|------|-------|--------|
| (vacío) | 0 | 0 | 1 | (vacío) |
| `1` | 1 | 1 | 19 | `1` |
| `11` | 2 | 1 | 53 | `1` |
| `111` | 3 | 2 | 109 | `11` |
| `1111` | 4 | 3 | 191 | `111` |
| `11111` | 5 | 5 | 331 | `11111` |
| `111111` | 6 | 8 | 585 | `11111111` |

## Ejemplo de Ejecución

```
============================================================
  SIMULADOR DE MÁQUINA DE TURING
  Cálculo de la Sucesión de Fibonacci
============================================================

Cargando configuración desde: maquinas/fibonacci.json
Máquina cargada: Máquina de Turing - Fibonacci (Cinta Única)
Descripción: Calcula F(n) usando una sola cinta.

============================================================
ENTRADA
============================================================
Ingrese n para calcular F(n) en notación unaria.
Ejemplos: '' (vacío) para F(0), '1' para F(1), '111' para F(3)
------------------------------------------------------------
Entrada (n en unario): 11111

============================================================
RESUMEN DE EJECUCIÓN
============================================================
Entrada (n):     '11111' (5 en unario)
Pasos totales:   331
Estado final:    qaccept
Aceptado:        Sí
Resultado:       '11111' (F(5) = 5)
============================================================

Cinta final: #xxxxx.;1;1;11;111;11111;
             (secuencia completa: 1, 1, 2, 3, 5)
```

## Análisis de Complejidad

La Máquina de Turing tiene una **complejidad temporal exponencial**:

$$T(n) = O(\varphi^n)$$

Donde $\varphi \approx 1.618$ es la proporción áurea (razón dorada).

### Crecimiento de Pasos

| n | F(n) | Pasos | Ratio |
|---|------|-------|-------|
| 5 | 5 | 331 | - |
| 6 | 8 | 585 | 1.77 |
| 7 | 13 | 1,105 | 1.89 |
| 8 | 21 | 2,255 | 2.04 |
| 9 | 34 | 4,971 | 2.20 |
| 10 | 55 | 11,641 | 2.34 |
| 11 | 89 | 28,449 | 2.44 |
| 12 | 144 | 71,443 | 2.51 |

El ratio converge hacia φ ≈ 1.618, confirmando el crecimiento exponencial.

Ver [ANALISIS_COMPLEJIDAD.md](documentacion/ANALISIS_COMPLEJIDAD.md) para el desarrollo matemático completo.

## Entregables

| # | Entregable | Archivo |
|---|------------|---------|
| 1 | Convenciones elegidas | [CONVENCIONES.md](documentacion/CONVENCIONES.md) |
| 2 | Diagrama de la MT | [DIAGRAMA_MT.md](documentacion/DIAGRAMA_MT.md) |
| 3 | Archivo de componentes | [fibonacci.json](maquinas/fibonacci.json) |
| 4 | Programa en Python | [src/](src/) |
| 5 | Análisis empírico | [resultados/](resultados/) |
| 6 | Notación asintótica | [ANALISIS_COMPLEJIDAD.md](documentacion/ANALISIS_COMPLEJIDAD.md) |

## Autores

- [Nombre del integrante 1]
- [Nombre del integrante 2]

## Licencia

Proyecto académico - Universidad [Nombre]
