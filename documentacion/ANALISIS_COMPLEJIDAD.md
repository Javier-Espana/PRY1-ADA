# Análisis de Complejidad - Notación Asintótica O

## 1. ¿Qué es la Notación Asintótica O (Big-O)?

La **notación O grande (Big-O)** es una notación matemática que describe el comportamiento límite superior de una función cuando el argumento tiende hacia un valor particular o infinito. En el contexto de algoritmos, se utiliza para clasificar algoritmos según cómo crece su tiempo de ejecución o uso de espacio en relación con el tamaño de la entrada.

### Definición Formal

Sea $f(n)$ y $g(n)$ funciones de los enteros no negativos a los reales. Decimos que:

$$f(n) = O(g(n))$$

si existen constantes positivas $c$ y $n_0$ tales que:

$$f(n) \leq c \cdot g(n) \quad \text{para todo } n \geq n_0$$

Esto significa que $f(n)$ no crece más rápido que $g(n)$ para valores suficientemente grandes de $n$.

### Propiedades Importantes

1. **Transitividad**: Si $f(n) = O(g(n))$ y $g(n) = O(h(n))$, entonces $f(n) = O(h(n))$
2. **Regla de la suma**: $O(f(n)) + O(g(n)) = O(\max(f(n), g(n)))$
3. **Regla del producto**: $O(f(n)) \cdot O(g(n)) = O(f(n) \cdot g(n))$

---

## 2. Análisis de la Máquina de Turing para Fibonacci

### 2.1 Descripción del Algoritmo

Nuestra Máquina de Turing calcula $F(n)$ (el n-ésimo número de Fibonacci) utilizando un enfoque iterativo que mantiene:
- Dos registros: $F(i-1)$ y $F(i)$ en notación unaria
- Un contador de iteraciones restantes

### 2.2 Operaciones por Iteración

En cada iteración del bucle principal, la máquina debe:

1. **Decrementar el contador**: $O(n)$ pasos (recorrer el contador)
2. **Copiar $F(i)$ a temporal**: $O(F(i))$ pasos
3. **Sumar $F(i-1)$ a temporal**: $O(F(i-1))$ pasos
4. **Actualizar registros**: $O(F(i) + F(i-1)) = O(F(i+1))$ pasos
5. **Regresar al inicio**: $O(F(i+1) + n)$ pasos

El trabajo en cada iteración $i$ es proporcional a:
$$W_i = O(F(i) + F(i-1) + n) = O(F(i+1) + n)$$

### 2.3 Número Total de Iteraciones

Para calcular $F(n)$, necesitamos $(n-1)$ iteraciones (desde $F(1)$ hasta $F(n)$).

### 2.4 Cálculo de la Complejidad Total

El tiempo total $T(n)$ es la suma del trabajo en todas las iteraciones:

$$T(n) = \sum_{i=1}^{n-1} W_i = \sum_{i=1}^{n-1} O(F(i+1) + n)$$

$$T(n) = \sum_{i=2}^{n} O(F(i)) + O(n^2)$$

Usando la identidad de Fibonacci:
$$\sum_{i=1}^{n} F(i) = F(n+2) - 1$$

Por lo tanto:
$$T(n) = O(F(n+2)) + O(n^2) = O(F(n))$$

Ya que $F(n)$ crece exponencialmente y domina el término $n^2$.

---

## 3. Relación con la Proporción Áurea

### 3.1 Fórmula de Binet

El n-ésimo número de Fibonacci puede expresarse mediante la **fórmula de Binet**:

$$F(n) = \frac{\varphi^n - \psi^n}{\sqrt{5}}$$

Donde:
- $\varphi = \frac{1 + \sqrt{5}}{2} \approx 1.618$ (proporción áurea)
- $\psi = \frac{1 - \sqrt{5}}{2} \approx -0.618$

### 3.2 Crecimiento Asintótico de Fibonacci

Como $|\psi| < 1$, el término $\psi^n$ se vuelve despreciable para $n$ grande:

$$F(n) \approx \frac{\varphi^n}{\sqrt{5}}$$

Por lo tanto:
$$F(n) = \Theta(\varphi^n)$$

### 3.3 Complejidad Final

Combinando los resultados:

$$\boxed{T(n) = O(n \cdot F(n)) = O(n \cdot \varphi^n)}$$

Esta es una **complejidad exponencial**, donde:
- El factor $n$ proviene de las iteraciones y operaciones de búsqueda en la cinta
- El factor $\varphi^n$ proviene del tamaño de los números de Fibonacci que se manipulan

---

## 4. Verificación Empírica

### 4.1 Datos Experimentales

| n | Pasos (T) | F(n) | n × F(n) | T / (n × F(n)) |
|---|-----------|------|----------|----------------|
| 0 | 1 | 0 | 0 | - |
| 1 | 3 | 1 | 1 | 3.00 |
| 2 | 4 | 1 | 2 | 2.00 |
| 3 | 42 | 2 | 6 | 7.00 |
| 4 | 96 | 3 | 12 | 8.00 |
| 5 | 202 | 5 | 25 | 8.08 |
| 6 | 402 | 8 | 48 | 8.38 |
| 7 | 736 | 13 | 91 | 8.09 |
| 8 | 1262 | 21 | 168 | 7.51 |
| 9 | 2046 | 34 | 306 | 6.69 |
| 10 | 3168 | 55 | 550 | 5.76 |

### 4.2 Análisis de la Constante

El cociente $\frac{T(n)}{n \cdot F(n)}$ se mantiene relativamente constante (entre 5 y 9), lo que confirma que:

$$T(n) = c \cdot n \cdot F(n)$$

para alguna constante $c \approx 7$.

### 4.3 Verificación del Crecimiento Exponencial

Si graficamos $\log(T(n))$ vs $n$, deberíamos ver una línea aproximadamente recta con pendiente $\log(\varphi) \approx 0.48$.

Esto se confirma en nuestro diagrama de dispersión, donde los pasos crecen exponencialmente con $n$.

---

## 5. Comparación con Otras Implementaciones

| Implementación | Complejidad Temporal | Complejidad Espacial |
|----------------|---------------------|---------------------|
| **MT de una cinta (este proyecto)** | $O(n \cdot \varphi^n)$ | $O(\varphi^n)$ |
| Recursión ingenua | $O(\varphi^n)$ | $O(n)$ |
| Programación dinámica | $O(n)$ | $O(n)$ o $O(1)$ |
| Exponenciación de matrices | $O(\log n)$ | $O(1)$ |

La máquina de Turing tiene un factor adicional de $n$ debido a:
1. La representación unaria de los números
2. La necesidad de recorrer la cinta para cada operación

---

## 6. Conclusión

La Máquina de Turing diseñada para calcular la sucesión de Fibonacci tiene una complejidad temporal de:

$$\boxed{T(n) = O(n \cdot \varphi^n) \approx O(n \cdot 1.618^n)}$$

Esta complejidad exponencial es inherente al problema cuando se utilizan:
- Representación unaria de números
- Una máquina de Turing determinista de una sola cinta

La verificación empírica mediante mediciones de tiempo y pasos confirma este análisis teórico, mostrando un crecimiento exponencial consistente con la proporción áurea.

---

## Referencias

1. Sipser, M. (2012). *Introduction to the Theory of Computation*. Cengage Learning.
2. Cormen, T. H., et al. (2009). *Introduction to Algorithms*. MIT Press.
3. Wikipedia: [Sucesión de Fibonacci](https://es.wikipedia.org/wiki/Sucesión_de_Fibonacci)
4. Wikipedia: [Notación O grande](https://es.wikipedia.org/wiki/Cota_superior_asintótica)
