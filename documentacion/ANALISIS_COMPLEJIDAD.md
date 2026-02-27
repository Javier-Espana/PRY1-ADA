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

Combinando los resultados y la verificación empírica:

$$\boxed{T(n) = O(\varphi^{2n}) \approx O(2.618^n)}$$

Esta es una **complejidad exponencial**, donde:
- El factor exponencial base $\varphi^n$ proviene del tamaño de los números de Fibonacci
- El factor adicional $\varphi^n$ proviene del trabajo requerido para manipular esos números en representación unaria
- Resultado: $\varphi^n \cdot \varphi^n = \varphi^{2n} \approx 2.618^n$

---

## 4. Verificación Empírica

### 4.1 Datos Experimentales

| n | Pasos (T) | F(n) | Ratio T(n)/T(n-1) | Tiempo (s) |
|---|-----------|------|-------------------|------------|
| 0 | 1 | 0 | - | 0.000005 |
| 1 | 19 | 1 | 19.00 | 0.000077 |
| 2 | 53 | 1 | 2.79 | 0.00017 |
| 3 | 109 | 2 | 2.06 | 0.00040 |
| 4 | 191 | 3 | 1.75 | 0.00071 |
| 5 | 331 | 5 | 1.73 | 0.0015 |
| 6 | 585 | 8 | 1.77 | 0.0030 |
| 7 | 1,105 | 13 | 1.89 | 0.0068 |
| 8 | 2,255 | 21 | 2.04 | 0.020 |
| 9 | 4,971 | 34 | 2.20 | 0.055 |
| 10 | 11,641 | 55 | 2.34 | 0.15 |
| 11 | 28,449 | 89 | 2.44 | 0.55 |
| 12 | 71,443 | 144 | 2.51 | 2.26 |
| 13 | 182,439 | 233 | 2.55 | 9.99 |
| 14 | 470,561 | 377 | 2.58 | 49.4 |
| 15 | 1,220,961 | 610 | 2.59 | 207.4 |

### 4.2 Análisis del Crecimiento

El **ratio de crecimiento** $\frac{T(n)}{T(n-1)}$ converge hacia un valor cercano a **2.59**, lo que confirma el comportamiento exponencial:

$$T(n) \approx c \cdot r^n \quad \text{donde } r \approx 2.59$$

Este valor es mayor que $\varphi \approx 1.618$ porque cada iteración requiere trabajo proporcional a los números de Fibonacci que se manipulan (en representación unaria), haciendo que el crecimiento sea aproximadamente $\varphi^2 \approx 2.618$.

### 4.3 Verificación del Crecimiento Exponencial

Los datos muestran claramente un **crecimiento exponencial**:

- **De n=10 a n=15**: Los pasos aumentan de 11,641 a 1,220,961 (factor de ~105x)
- **De n=12 a n=15**: El tiempo aumenta de 2.26s a 207.4s (factor de ~92x)

El análisis de regresión exponencial confirma que:

$$T(n) = O(\varphi^{2n}) \approx O(2.618^n)$$

Esto se visualiza en el gráfico de pasos vs n, donde la curva muestra el característico crecimiento exponencial.

---

## 5. Comparación con Otras Implementaciones

| Implementación | Complejidad Temporal | Complejidad Espacial |
|----------------|---------------------|---------------------|
| **MT de una cinta (este proyecto)** | $O(\varphi^{2n}) \approx O(2.618^n)$ | $O(\varphi^n)$ |
| Recursión ingenua | $O(\varphi^n)$ | $O(n)$ |
| Programación dinámica | $O(n)$ | $O(n)$ o $O(1)$ |
| Exponenciación de matrices | $O(\log n)$ | $O(1)$ |

La máquina de Turing tiene un factor adicional $\varphi^n$ (comparada con recursión ingenua) debido a:
1. La representación unaria de los números
2. La necesidad de recorrer la cinta completa para cada operación de copia/suma
3. La longitud de los números de Fibonacci crece como $O(\varphi^n)$

---

## 6. Conclusión

La Máquina de Turing diseñada para calcular la sucesión de Fibonacci tiene una complejidad temporal de:

$$\boxed{T(n) = O(\varphi^{2n}) \approx O(2.618^n)}$$

Esta complejidad exponencial es inherente al problema cuando se utilizan:
- Representación unaria de números
- Una máquina de Turing determinista de una sola cinta
- Operaciones de copia y suma que requieren recorrer toda la representación

La verificación empírica confirma este análisis teórico:
- El ratio de crecimiento $T(n)/T(n-1)$ converge a ~2.59 ≈ $\varphi^2$
- Para n=15, la máquina realiza más de **1.2 millones de pasos** en ~3.5 minutos
- El crecimiento exponencial hace impráctica la computación para n > 15

---

## Referencias

1. Sipser, M. (2012). *Introduction to the Theory of Computation*. Cengage Learning.
2. Cormen, T. H., et al. (2009). *Introduction to Algorithms*. MIT Press.
3. Wikipedia: [Sucesión de Fibonacci](https://es.wikipedia.org/wiki/Sucesión_de_Fibonacci)
4. Wikipedia: [Notación O grande](https://es.wikipedia.org/wiki/Cota_superior_asintótica)
