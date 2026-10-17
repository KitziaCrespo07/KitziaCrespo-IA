# Función heurística - 8-Puzzle con A*

**Inteligencia Artificial. Unidad 1**

Se implementan dos funciones heurísticas para resolver el 8-Puzzle mediante el algoritmo A*, con el propósito de comparar su eficiencia.

## Funciones heurísticas

Las heurísticas estiman cuántos movimientos faltan para alcanzar el estado objetivo. Se implementaron en `Heuristica.java`:

- **Fichas fuera de lugar:** cuenta las fichas que no están en su posición correcta.
- **Distancia Manhattan:** suma las distancias horizontales y verticales de cada ficha hasta su posición objetivo.

Ambas excluyen el espacio vacío y nunca estiman más movimientos de los realmente necesarios.

## Algoritmo A*

A* utiliza **f(n) = g(n) + h(n)**, donde `g(n)` representa el costo acumulado y `h(n)` la estimación heurística. Así, prioriza los estados con menor costo total estimado.

## Ejecución

```bash
javac -d bin src/*.java
java -cp bin App
```

## Resultados

Con el estado inicial `7621 3458` y el objetivo `12345678 `, ambas heurísticas encontraron la solución óptima de **18 movimientos**.

La heurística de fichas fuera de lugar visitó **1,796 estados**, mientras que la distancia Manhattan visitó **385**, lo que demostró una mayor eficiencia al explorar menos estados.

**Nota:** `Time` representa los nodos extraídos de la cola, incluidos los repetidos. El tiempo real de ejecución se muestra por separado en milisegundos.