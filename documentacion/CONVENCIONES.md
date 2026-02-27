# Convenciones para la Máquina de Turing - Sucesión de Fibonacci

## 1. Representación de Enteros No Negativos en la Cinta

### Convención Unaria
Los números enteros no negativos se representan en **notación unaria** utilizando el símbolo `1`:

| Número | Representación |
|--------|----------------|
| 0      | (vacío)        |
| 1      | 1              |
| 2      | 11             |
| 3      | 111            |
| n      | n unos         |

### Justificación
- La notación unaria es natural para máquinas de Turing básicas
- Facilita operaciones de suma (concatenación)
- Permite visualizar fácilmente el proceso de cálculo

## 2. Alfabeto de la Cinta

| Símbolo | Significado |
|---------|-------------|
| `1`     | Dígito unario (representa cantidad) |
| `_`     | Blanco (símbolo por defecto) |
| `#`     | Marcador de inicio de cinta |
| `.`     | Separador zona de contador y trabajo |
| `;`     | Separador entre términos Fibonacci |
| `x`     | Contador usado/procesado |
| `y`     | Marcador temporal copiando término 1 |
| `z`     | Marcador temporal copiando término 2 |

## 3. Formato de Entrada

La entrada `n` indica que queremos calcular F(n), el n-ésimo número de Fibonacci.

**Formato:** `111...1` (n unos)

**Ejemplos:**
- Para calcular F(0): entrada vacía o `_`
- Para calcular F(1): `1`
- Para calcular F(5): `11111`

## 4. Formato de Salida

Al finalizar la ejecución, la cinta contendrá toda la secuencia calculada hasta F(n).
El resultado F(n) se extrae del último término de la secuencia.

**Formato de la cinta final:** `#xxx...x.;1;1;11;111;...;F(n);`

**Ejemplos de resultados esperados:**
| Entrada (n) | F(n) | Salida (unaria) |
|-------------|------|-----------------|
| (vacío)     | 0    | (vacío)         |
| 1           | 1    | 1               |
| 11          | 1    | 1               |
| 111         | 2    | 11              |
| 1111        | 3    | 111             |
| 11111       | 5    | 11111           |
| 111111      | 8    | 11111111        |

## 5. Estructura de la Cinta Durante el Cálculo

Durante la ejecución, la cinta mantiene el formato:
```
#[contador].[término1];[término2];...;[términoN];
```

Donde:
- `#`: Marcador de inicio
- `contador`: Caracteres `x` que indican iteraciones consumidas, `1` las restantes
- `.`: Separador entre zona de contador y zona de trabajo
- `términoK`: Número de Fibonacci k-ésimo en notación unaria
- `;`: Separadores entre términos

**Nota sobre la secuencia:** Esta máquina calcula la secuencia 1, 1, 2, 3, 5, 8... 
(omitiendo F(0)=0 por convención de implementación)

## 6. Verificación de Paridad

Al inicio, la máquina realiza una verificación de paridad del número de entrada
usando estados alternantes (`qParE` y `qParO`) en lugar de memoria cache.
Esto permite determinar si n es par o impar antes de iniciar el cálculo.

## 7. Posición Inicial de la Cabeza

La cabeza lectora/escritora comienza en la **posición más a la izquierda** de la entrada.

## 8. Estados Especiales

- **q0**: Estado inicial
- **qaccept**: Estado de aceptación (cálculo completado)

## 9. Dirección del Movimiento

| Símbolo | Dirección |
|---------|-----------|
| `R`     | Derecha   |
| `L`     | Izquierda |
| `S`     | Sin movimiento |

---

## Sucesión de Fibonacci - Definición

```
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2) para n ≥ 2
```

**Primeros términos:** 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...

## Complejidad de la Máquina

Esta implementación de cinta única tiene complejidad temporal **exponencial** O(φ^n)
donde φ ≈ 1.618 (razón áurea), debido a:
- Múltiples recorridos de la cinta para cada iteración
- Copia término a término de los valores Fibonacci
- Crecimiento exponencial del tamaño de los términos
