# 8-puzzle – Búsquedas no informadas

Entregable del primer parcial. Inteligencia Artificial, Unidad 1.

El programa resuelve el 8-puzzle con las cinco búsquedas no informadas del entregable y con la búsqueda bidireccional (opcional). Al final de cada una imprime la ruta de solución y sus datos estadísticos.

- Primero en anchura (`breadthFirstSearch`)
- Costo uniforme (`uniformCostSearch`)
- Primero en profundidad (`depthFirstSearch`)
- Profundidad limitada (`depthLimitedSearch`)
- Profundidad iterativa (`iterativeDeepeningSearch`)
- Bidireccional, opcional (`bidirectionalSearch`)

**Estado inicial:** `7621 3458`  **Estado objetivo:** `12345678 `

## Compilar y ejecutar

```
javac -d bin src/*.java
java -cp bin App
```

## Tabla comparativa

Los resultados experimentales de cada búsqueda, comparados con los criterios teóricos del libro, están en `Kitzia Crespo. IA. U1. Tabla Comparativa - Entregable Primer Parcial.pdf`.
