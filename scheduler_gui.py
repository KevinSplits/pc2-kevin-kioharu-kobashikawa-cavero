#!/usr/bin/env python3
"""
Simulador y comparador de algoritmos de planificación en la nube con interfaz gráfica.
Compara FCFS vs Min-Min con 50 tareas y 5 VMs con distintas capacidades.
"""

import random
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------------- CONFIGURACIÓN Y DATASET ----------------------

def generar_dataset(semilla=42):
    """Genera 50 tareas con duraciones base aleatorias y 5 VMs con velocidades distintas."""
    random.seed(semilla)
    # 50 tareas con duraciones base entre 10 y 100 unidades
    duraciones_base = [random.randint(10, 100) for _ in range(50)]
    
    # 5 VMs con multiplicadores de velocidad (0.5 = muy rápida, 1.5 = lenta)
    vm_velocidades = [0.5, 0.75, 1.0, 1.25, 1.5]
    vm_nombres = [f"VM-{i+1}" for i in range(5)]
    
    return duraciones_base, vm_velocidades, vm_nombres


# ---------------------- ALGORITMOS DE SCHEDULING ----------------------

def algoritmo_fcfs(duraciones_base, vm_velocidades):
    """
    Algoritmo FCFS: asigna tareas en el orden en que llegan a la primera VM que se desocupe.
    Retorna (makespan, tiempo_espera_promedio, cronograma_vm).
    """
    tiempo_vm = [0.0] * len(vm_velocidades)
    cronograma = [[] for _ in range(len(vm_velocidades))]
    tiempo_espera_total = 0
    
    for i, dur_base in enumerate(duraciones_base):
        # Encontrar la VM que se desocupe primero (menor tiempo de disponibilidad)
        idx_vm = tiempo_vm.index(min(tiempo_vm))
        
        # Tiempo de ejecución en esta VM
        ejecucion = dur_base * vm_velocidades[idx_vm]
        
        # Tiempo de inicio = tiempo actual de la VM
        tiempo_esperado = tiempo_vm[idx_vm]
        tiempo_espera_total += tiempo_esperado
        
        # La tarea termina en:
        fin_tarea = tiempo_esperado + ejecucion
        
        # Actualizar disponibilidad de la VM
        tiempo_vm[idx_vm] = fin_tarea
        
        cronograma[idx_vm].append({
            "tarea": i,
            "duracion_base": dur_base,
            "vm": idx_vm,
            "tiempo_espera": tiempo_esperado,
            "tiempo_ejecucion": ejecucion,
            "tiempo_fin": fin_tarea
        })
    
    makespan = max(tiempo_vm)
    tiempo_espera_promedio = tiempo_espera_total / len(duraciones_base)
    
    return makespan, tiempo_espera_promedio, cronograma


def algoritmo_min_min(duraciones_base, vm_velocidades):
    """
    Algoritmo Min-Min: evalúa todas las tareas pendientes, calcula el tiempo estimado
    de finalización en cada recurso, y asigna primero la tarea más corta al recurso 
    que la termine más rápido.
    Retorna (makespan, tiempo_espera_promedio, cronograma_vm).
    """
    tareas_pendientes = list(range(len(duraciones_base)))
    tiempo_vm = [0.0] * len(vm_velocidades)
    cronograma = [[] for _ in range(len(vm_velocidades))]
    tiempo_espera_total = 0
    
    while tareas_pendientes:
        # Evaluar todas las tareas pendientes
        mejores_opciones = []
        
        for idx_tarea in tareas_pendientes:
            dur_base = duraciones_base[idx_tarea]
            opciones = []
            
            for idx_vm, vel in enumerate(vm_velocidades):
                # Tiempo de ejecución en esta VM
                ejecucion = dur_base * vel
                # Tiempo de finalización si asignamos ahora
                fin_tarea = tiempo_vm[idx_vm] + ejecucion
                opciones.append((fin_tarea, idx_vm))
            
            # Elegir la VM que termine esta tarea más rápido
            fin_min, idx_vm_opt = min(opciones, key=lambda x: x[0])
            mejores_opciones.append((dur_base, fin_min, idx_tarea, idx_vm_opt))
        
        # De todas las tareas pendientes, elegir la que tiene el tiempo de finalización más corto
        dur_base_seleccionada, fin_seleccionado, idx_tarea_seleccionada, idx_vm_seleccionada = min(
            mejores_opciones, key=lambda x: x[1]
        )
        
        # Ejecutar la tarea seleccionada
        tiempo_esperado = tiempo_vm[idx_vm_seleccionada]
        tiempo_espera_total += tiempo_esperado
        
        ejecucion = dur_base_seleccionada * vm_velocidades[idx_vm_seleccionada]
        fin_tarea = tiempo_esperado + ejecucion
        
        tiempo_vm[idx_vm_seleccionada] = fin_tarea
        
        cronograma[idx_vm_seleccionada].append({
            "tarea": idx_tarea_seleccionada,
            "duracion_base": dur_base_seleccionada,
            "vm": idx_vm_seleccionada,
            "tiempo_espera": tiempo_esperado,
            "tiempo_ejecucion": ejecucion,
            "tiempo_fin": fin_tarea
        })
        
        # Remover tarea de la lista pendiente
        tareas_pendientes.remove(idx_tarea_seleccionada)
    
    makespan = max(tiempo_vm)
    tiempo_espera_promedio = tiempo_espera_total / len(duraciones_base)
    
    return makespan, tiempo_espera_promedio, cronograma


# ---------------------- INTERFAZ GRÁFICA ----------------------

class SchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Algoritmos de Scheduling en la Nube")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Variable de semilla
        self.semilla_var = tk.IntVar(value=42)
        
        # Frame superior: controles
        frame_superior = ttk.LabelFrame(root, text=" Configuración ", padding=10)
        frame_superior.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_superior, text="Semilla aleatoria:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(frame_superior, textvariable=self.semilla_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_superior, text="Ejecutar simulación", command=self.ejecutar_simulacion).pack(side=tk.LEFT, padx=10)
        
        # Frame central: resultados numéricos
        frame_resultados = ttk.LabelFrame(root, text=" Métricas Clave ", padding=10)
        frame_resultados.pack(fill=tk.X, padx=10, pady=5)
        
        # Resultados FCFS
        ttk.Label(frame_resultados, text="FCFS:").grid(row=0, column=0, padx=5, pady=2)
        self.label_fcfs_makespan = ttk.Label(frame_resultados, text="--")
        self.label_fcfs_makespan.grid(row=0, column=1, padx=5, pady=2)
        self.label_fcfs_espera = ttk.Label(frame_resultados, text="--")
        self.label_fcfs_espera.grid(row=0, column=2, padx=5, pady=2)
        
        # Resultados Min-Min
        ttk.Label(frame_resultados, text="Min-Min:").grid(row=1, column=0, padx=5, pady=2)
        self.label_minmin_makespan = ttk.Label(frame_resultados, text="--")
        self.label_minmin_makespan.grid(row=1, column=1, padx=5, pady=2)
        self.label_minmin_espera = ttk.Label(frame_resultados, text="--")
        self.label_minmin_espera.grid(row=1, column=2, padx=5, pady=2)
        
        # Frame inferior: gráficas
        frame_grafica = ttk.LabelFrame(root, text=" Comparación Visual ", padding=10)
        frame_grafica.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.fig, self.axes = plt.subplots(1, 2, figsize=(10, 4))
        self.fig.tight_layout(pad=3.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_grafica)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def ejecutar_simulacion(self):
        """Ejecuta la simulación completa y actualiza la interfaz."""
        semilla = self.semilla_var.get()
        random.seed(semilla)
        
        # Generar dataset
        duraciones_base, vm_velocidades, vm_nombres = generar_dataset(semilla)
        
        # Ejecutar algoritmos
        makespan_fcfs, espera_fcfs, _ = algoritmo_fcfs(duraciones_base, vm_velocidades)
        makespan_minmin, espera_minmin, _ = algoritmo_min_min(duraciones_base, vm_velocidades)
        
        # Actualizar etiquetas numéricas
        self.label_fcfs_makespan.config(text=f"{makespan_fcfs:.2f}")
        self.label_fcfs_espera.config(text=f"{espera_fcfs:.2f}")
        self.label_minmin_makespan.config(text=f"{makespan_minmin:.2f}")
        self.label_minmin_espera.config(text=f"{espera_minmin:.2f}")
        
        # Actualizar gráficas
        self.actualizar_graficas(makespan_fcfs, makespan_minmin, espera_fcfs, espera_minmin)
        
        # Mostrar análisis en mensaje
        self.mostrar_analisis(makespan_fcfs, makespan_minmin, espera_fcfs, espera_minmin)
    
    def actualizar_graficas(self, m_fcfs, m_minmin, e_fcfs, e_minmin):
        """Actualiza los subgráficos de comparación."""
        self.axes[0].clear()
        self.axes[1].clear()
        
        algoritmos = ['FCFS', 'Min-Min']
        colores = ['skyblue', 'orange']
        
        # Subgráfico 1: Makespan
        self.axes[0].bar(algoritmos, [m_fcfs, m_minmin], color=colores, edgecolor='black')
        self.axes[0].set_title('Makespan', fontsize=12)
        self.axes[0].set_ylabel('Tiempo (unidades)')
        
        # Subgráfico 2: Tiempo de espera promedio
        self.axes[1].bar(algoritmos, [e_fcfs, e_minmin], color=colores, edgecolor='black')
        self.axes[1].set_title('Tiempo de Espera Promedio', fontsize=12)
        self.axes[1].set_ylabel('Tiempo (unidades)')
        
        self.canvas.draw()
    
    def mostrar_analisis(self, m_fcfs, m_minmin, e_fcfs, e_minmin):
        """Muestra el análisis de resultados en un messagebox."""
        analysis = "=" * 50 + "\nRESULTADOS DE LA SIMULACIÓN\n" + "=" * 50
        
        # Determinar qué algoritmo terminó antes
        if m_minmin < m_fcfs:
            ganador_makespan = "Min-Min"
            mejora_makespan = f"{(1 - m_minmin/m_fcfs)*100:.1f}% más rápido"
        else:
            ganador_makespan = "FCFS"
            mejora_makespan = f"{(m_fcfs - m_minmin):.2f} unidades más rápido"
        
        # Determinar qué algoritmo aprovechó mejor la CPU
        if e_minmin < e_fcfs:
            ganador_espera = "Min-Min"
            mejora_espera = f"{(1 - e_minmin/e_fcfs)*100:.1f}% menos tiempo de espera"
        else:
            ganador_espera = "FCFS"
            mejora_espera = f"{(e_fcfs - e_minmin):.2f} unidades menos tiempo de espera"
        
        analysis += f"\n📊 MAKESPAN:\n"
        analysis += f"   FCFS: {m_fcfs:.2f} | Min-Min: {m_minmin:.2f}\n"
        analysis += f"   → Ganador: {ganador_makespan} ({mejora_makespan})\n"
        
        analysis += f"\n⏱️ TIEMPO DE ESPERA PROMEDIO:\n"
        analysis += f"   FCFS: {e_fcfs:.2f} | Min-Min: {e_minmin:.2f}\n"
        analysis += f"   → Ganador: {ganador_espera} ({mejora_espera})\n"
        
        analysis += "=" * 50
        
        messagebox.showinfo("Análisis de Resultados", analysis)


# ---------------------- PUNTO DE ENTRADA ----------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulingApp(root)
    root.mainloop()