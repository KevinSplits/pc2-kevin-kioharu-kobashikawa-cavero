# PC2 - Simulador de Scheduling en la Nube

## Hecho por: Kevin Kioharu Kobashikawa Cavero

---

## Descripción

Este repositorio contiene un script Python completo para simular y comparar el rendimiento de dos algoritmos de planificación (scheduling) en la nube:

- **FCFS (First-Come, First-Served)**: Asigna tareas en el orden en que llegan a la primera VM disponible.
- **Min-Min**: Evalúa todas las tareas pendientes, calcula el tiempo estimado de finalización en cada recurso y asigna primero la tarea más corta al recurso que la termine más rápido.

## Dataset

- **50 tareas (jobs)** con diferentes tamaños o duraciones base generadas aleatoriamente.
- **5 máquinas virtuales (VMs)** con distintas capacidades de procesamiento definidas por multiplicadores de velocidad (0.5, 0.75, 1.0, 1.25, 1.5), donde un multiplicador menor indica una VM más rápida.

## Métricas calculadas

Para cada algoritmo, el script calcula y registra:

1. **Makespan**: El tiempo total hasta que se completa la última tarea.
2. **Tiempo de espera promedio**: El promedio de los tiempos de espera de todas las tareas.

## Graficación

Utiliza la librería `matplotlib` para generar un gráfico de barras (dos subgráficos) que compara visualmente el makespan y el tiempo de espera entre FCFS y Min-Min.

## Resultados esperados

El script imprime en la consola los resultados numéricos y un breve análisis en texto que responde:

- ¿Cuál de los dos algoritmos logró terminar antes? (comparación de makespan)
- ¿Cuál aprovechó mejor la CPU de las máquinas virtuales? (comparación de tiempo de espera promedio)

## Ejecución

El script se ejecuta de forma local y requiere solo la librería `matplotlib` para la graficación (las demás dependencias son estándar de Python).

## Objetivo de laboratorio

Cumple con los requerimientos de la guía de laboratorio de Cloud Computing para la comparación y análisis de algoritmos de scheduling en entornos simulados.