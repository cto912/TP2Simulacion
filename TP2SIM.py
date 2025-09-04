#TRABAJO PRACTICO N2 SIMULACION -GENERADOR DE NUMEROS RANDOM-
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import random
import math
import os
import sys
from datetime import datetime
import psutil  # Para verificar memoria disponible

class RandomNumberGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Números Aleatorios - TP2 Simulación")
        self.root.geometry("1200x800")
        
        # Variables para almacenar los datos generados
        self.generated_numbers = []
        self.frequency_table = None
        self.generation_parameters = {}  # Para almacenar parámetros de generación
        
        # Configurar la interfaz
        self.setup_ui()
        
    def check_memory_availability(self, sample_size):
        """Verifica si hay suficiente memoria para la muestra solicitada"""
        try:
            # Estimar memoria necesaria (aproximadamente 8 bytes por número float + overhead)
            estimated_memory_mb = (sample_size * 8) / (1024 * 1024) * 2  # Factor 2 para overhead
            available_memory_mb = psutil.virtual_memory().available / (1024 * 1024)
            
            if estimated_memory_mb > available_memory_mb * 0.8:  # Usar max 80% de memoria disponible
                return False, f"Memoria insuficiente. Necesario: {estimated_memory_mb:.1f}MB, Disponible: {available_memory_mb:.1f}MB"
            return True, "OK"
        except:
            # Si hay error al verificar memoria, permitir pero con advertencia
            return True, "No se pudo verificar memoria disponible"
    
    def validate_numeric_input(self, value_str, field_name, min_val=None, max_val=None, allow_zero=False):
        """Valida entrada numérica con rango opcional"""
        try:
            value = float(value_str.strip())
            
            # Verificar si es un número válido
            if math.isnan(value) or math.isinf(value):
                return False, f"{field_name} debe ser un número finito válido"
            
            # Verificar rango mínimo
            if min_val is not None:
                if not allow_zero and value <= min_val:
                    return False, f"{field_name} debe ser mayor que {min_val}"
                elif allow_zero and value < min_val:
                    return False, f"{field_name} debe ser mayor o igual que {min_val}"
            
            # Verificar rango máximo
            if max_val is not None and value > max_val:
                return False, f"{field_name} debe ser menor o igual que {max_val}"
                
            return True, value
        except ValueError:
            return False, f"{field_name} debe ser un número válido"
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Generador de Números Aleatorios", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="10")
        config_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        # Tamaño de muestra
        ttk.Label(config_frame, text="Tamaño de muestra:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.sample_size_var = tk.StringVar(value="1000")
        sample_size_entry = ttk.Entry(config_frame, textvariable=self.sample_size_var, width=15)
        sample_size_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        ttk.Label(config_frame, text="(máx: 1,000,000)").grid(row=0, column=2, sticky=tk.W, padx=(5, 0), pady=5)
        
        # Selección de distribución
        ttk.Label(config_frame, text="Distribución:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.distribution_var = tk.StringVar(value="Uniforme")
        distribution_combo = ttk.Combobox(config_frame, textvariable=self.distribution_var,
                                        values=["Uniforme", "Exponencial", "Normal"],
                                        state="readonly", width=12)
        distribution_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        distribution_combo.bind("<<ComboboxSelected>>", self.on_distribution_change)
        
        # Frame para parámetros de distribución
        self.params_frame = ttk.LabelFrame(config_frame, text="Parámetros", padding="10")
        self.params_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Número de intervalos
        ttk.Label(config_frame, text="Intervalos:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.intervals_var = tk.StringVar(value="10")
        intervals_combo = ttk.Combobox(config_frame, textvariable=self.intervals_var,
                                     values=["5", "10", "15", "20", "25"],
                                     state="readonly", width=12)
        intervals_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Botón generar
        generate_btn = ttk.Button(config_frame, text="Generar Números", 
                                command=self.generate_numbers)
        generate_btn.grid(row=4, column=0, columnspan=3, pady=(20, 0))
        
        # Configurar parámetros iniciales
        self.setup_parameters()
        
        # Frame de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Pestaña de datos
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="Datos Generados")
        
        # Pestaña de histograma
        self.histogram_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.histogram_frame, text="Histograma")
        
        # Pestaña de tabla de frecuencias
        self.freq_table_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.freq_table_frame, text="Tabla de Frecuencias")
        
        # Configurar cada pestaña
        self.setup_data_tab()
        self.setup_histogram_tab()
        self.setup_frequency_table_tab()
        
    def setup_parameters(self):
        # Limpiar frame de parámetros
        for widget in self.params_frame.winfo_children():
            widget.destroy()
            
        distribution = self.distribution_var.get()
        
        if distribution == "Uniforme":
            ttk.Label(self.params_frame, text="a (límite inferior):").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.param_a_var = tk.StringVar(value="0")
            ttk.Entry(self.params_frame, textvariable=self.param_a_var, width=10).grid(row=0, column=1, padx=(5, 10), pady=2)
            
            ttk.Label(self.params_frame, text="b (límite superior):").grid(row=0, column=2, sticky=tk.W, pady=2)
            self.param_b_var = tk.StringVar(value="1")
            ttk.Entry(self.params_frame, textvariable=self.param_b_var, width=10).grid(row=0, column=3, padx=(5, 0), pady=2)
            
        elif distribution == "Exponencial":
            ttk.Label(self.params_frame, text="λ (lambda):").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.param_lambda_var = tk.StringVar(value="1")
            ttk.Entry(self.params_frame, textvariable=self.param_lambda_var, width=10).grid(row=0, column=1, padx=(5, 0), pady=2)
            
        elif distribution == "Normal":
            ttk.Label(self.params_frame, text="μ (media):").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.param_mu_var = tk.StringVar(value="0")
            ttk.Entry(self.params_frame, textvariable=self.param_mu_var, width=10).grid(row=0, column=1, padx=(5, 10), pady=2)
            
            ttk.Label(self.params_frame, text="σ (desv. estándar):").grid(row=0, column=2, sticky=tk.W, pady=2)
            self.param_sigma_var = tk.StringVar(value="1")
            ttk.Entry(self.params_frame, textvariable=self.param_sigma_var, width=10).grid(row=0, column=3, padx=(5, 0), pady=2)
    
    def on_distribution_change(self, event):
        self.setup_parameters()
    
    def setup_data_tab(self):
        # Área de texto para mostrar los datos
        data_label = ttk.Label(self.data_frame, text="Números generados (4 decimales):")
        data_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.data_text = scrolledtext.ScrolledText(self.data_frame, height=15, width=60)
        self.data_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Botón para copiar datos
        copy_data_btn = ttk.Button(self.data_frame, text="Copiar Datos", 
                                 command=self.copy_data)
        copy_data_btn.pack(anchor=tk.W)
        
    def setup_histogram_tab(self):
        # Frame para el gráfico
        self.histogram_canvas_frame = ttk.Frame(self.histogram_frame)
        self.histogram_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
    def setup_frequency_table_tab(self):
        # Tabla de frecuencias
        freq_label = ttk.Label(self.freq_table_frame, text="Tabla de Frecuencias:")
        freq_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Treeview para la tabla
        columns = ("Intervalo", "Límite Inf", "Límite Sup", "Frecuencia", "Freq. Relativa", "Freq. Acumulada")
        self.freq_tree = ttk.Treeview(self.freq_table_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.freq_tree.heading(col, text=col)
            self.freq_tree.column(col, width=100, anchor=tk.CENTER)
            
        # Scrollbar para la tabla
        freq_scrollbar = ttk.Scrollbar(self.freq_table_frame, orient=tk.VERTICAL, command=self.freq_tree.yview)
        self.freq_tree.configure(yscrollcommand=freq_scrollbar.set)
        
        self.freq_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 10))
        freq_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 10))
        
        # Botón para copiar tabla
        copy_table_btn = ttk.Button(self.freq_table_frame, text="Copiar Tabla", 
                                  command=self.copy_frequency_table)
        copy_table_btn.pack(side=tk.LEFT, anchor=tk.W, padx=(0, 10))
        
        # Botón para exportar a Excel
        export_excel_btn = ttk.Button(self.freq_table_frame, text="Exportar a Excel", 
                                    command=self.export_to_excel)
        export_excel_btn.pack(side=tk.LEFT, anchor=tk.W)
    
    def generate_numbers(self):
        try:
            # Validar tamaño de muestra
            is_valid, result = self.validate_numeric_input(
                self.sample_size_var.get(), 
                "Tamaño de muestra", 
                min_val=0, 
                max_val=1000000
            )
            if not is_valid:
                messagebox.showerror("Error de Validación", result)
                return
            
            sample_size = int(result)
            
            # Verificar memoria disponible
            memory_ok, memory_msg = self.check_memory_availability(sample_size)
            if not memory_ok:
                messagebox.showerror("Error de Memoria", memory_msg)
                return
            elif memory_msg != "OK":
                messagebox.showwarning("Advertencia", memory_msg)
                
            # Obtener y validar parámetros según la distribución
            distribution = self.distribution_var.get()
            
            if distribution == "Uniforme":
                # Validar parámetro a
                is_valid, a = self.validate_numeric_input(
                    self.param_a_var.get(), 
                    "Límite inferior (a)"
                )
                if not is_valid:
                    messagebox.showerror("Error de Validación", a)
                    return
                
                # Validar parámetro b
                is_valid, b = self.validate_numeric_input(
                    self.param_b_var.get(), 
                    "Límite superior (b)"
                )
                if not is_valid:
                    messagebox.showerror("Error de Validación", b)
                    return
                
                # Validar relación a < b
                if a >= b:
                    messagebox.showerror("Error de Validación", 
                                       f"El límite inferior ({a}) debe ser menor que el superior ({b})")
                    return
                
                self.generation_parameters = {"distribución": "Uniforme", "a": a, "b": b}
                self.generated_numbers = self.generate_uniform(sample_size, a, b)
                
            elif distribution == "Exponencial":
                # Validar parámetro lambda
                is_valid, lambda_param = self.validate_numeric_input(
                    self.param_lambda_var.get(), 
                    "Lambda (λ)", 
                    min_val=0
                )
                if not is_valid:
                    messagebox.showerror("Error de Validación", lambda_param)
                    return
                
                self.generation_parameters = {"distribución": "Exponencial", "lambda": lambda_param}
                self.generated_numbers = self.generate_exponential(sample_size, lambda_param)
                
            elif distribution == "Normal":
                # Validar parámetro mu
                is_valid, mu = self.validate_numeric_input(
                    self.param_mu_var.get(), 
                    "Media (μ)"
                )
                if not is_valid:
                    messagebox.showerror("Error de Validación", mu)
                    return
                
                # Validar parámetro sigma
                is_valid, sigma = self.validate_numeric_input(
                    self.param_sigma_var.get(), 
                    "Desviación estándar (σ)", 
                    min_val=0
                )
                if not is_valid:
                    messagebox.showerror("Error de Validación", sigma)
                    return
                
                self.generation_parameters = {"distribución": "Normal", "mu": mu, "sigma": sigma}
                self.generated_numbers = self.generate_normal(sample_size, mu, sigma)
            
            # Agregar información de generación
            self.generation_parameters.update({
                "tamaño_muestra": sample_size,
                "fecha_generación": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "intervalos": int(self.intervals_var.get())
            })
            
            # Actualizar visualizaciones
            self.update_data_display()
            self.update_histogram()
            self.update_frequency_table()
            
            # Calcular estadísticas para verificación
            mean_generated = np.mean(self.generated_numbers)
            std_generated = np.std(self.generated_numbers, ddof=1)
            
            # Mostrar mensaje de éxito con estadísticas
            success_msg = f"¡Generación exitosa!\n\n"
            success_msg += f"Números generados: {sample_size:,}\n"
            success_msg += f"Media observada: {mean_generated:.4f}\n"
            success_msg += f"Desviación estándar: {std_generated:.4f}\n\n"
            
            # Agregar valores teóricos esperados
            if distribution == "Uniforme":
                theoretical_mean = (a + b) / 2
                theoretical_std = math.sqrt((b - a)**2 / 12)
                success_msg += f"Media teórica: {theoretical_mean:.4f}\n"
                success_msg += f"Desv. est. teórica: {theoretical_std:.4f}"
            elif distribution == "Exponencial":
                theoretical_mean = 1 / lambda_param
                theoretical_std = 1 / lambda_param
                success_msg += f"Media teórica: {theoretical_mean:.4f}\n"
                success_msg += f"Desv. est. teórica: {theoretical_std:.4f}"
            elif distribution == "Normal":
                success_msg += f"Media teórica: {mu:.4f}\n"
                success_msg += f"Desv. est. teórica: {sigma:.4f}"
                
            messagebox.showinfo("Generación Completada", success_msg)
            
        except MemoryError:
            messagebox.showerror("Error de Memoria", 
                               "No hay suficiente memoria para generar esta cantidad de números. "
                               "Intente con un tamaño de muestra menor.")
        except Exception as e:
            messagebox.showerror("Error Inesperado", 
                               f"Se produjo un error inesperado:\n{str(e)}\n\n"
                               f"Por favor, verifique sus parámetros e intente nuevamente.")
            # Log del error para debugging
            print(f"Error en generate_numbers: {e}")
            import traceback
            traceback.print_exc()
    
    def generate_uniform(self, n, a, b):
        """Genera números aleatorios con distribución uniforme [a,b]
        
        Utiliza el método de transformación lineal:
        Si U ~ Uniforme(0,1), entonces X = a + (b-a)*U ~ Uniforme(a,b)
        """
        numbers = []
        try:
            for i in range(n):
                # Usar la función nativa del lenguaje para generar uniforme [0,1]
                u = random.random()
                # Transformar a [a,b]
                x = a + (b - a) * u
                numbers.append(round(x, 4))
                
                # Mostrar progreso para muestras grandes
                if n > 50000 and i % 10000 == 0:
                    progress = (i / n) * 100
                    print(f"Progreso: {progress:.1f}%")
                    
        except Exception as e:
            raise Exception(f"Error generando distribución uniforme: {str(e)}")
            
        return numbers
    
    def generate_exponential(self, n, lambda_param):
        """Genera números aleatorios con distribución exponencial
        
        Utiliza el método de transformación inversa:
        Si U ~ Uniforme(0,1), entonces X = -ln(1-U)/λ ~ Exponencial(λ)
        """
        numbers = []
        try:
            for i in range(n):
                u = random.random()
                # Método de transformación inversa
                # Usamos 1-u en lugar de u para evitar log(0)
                x = -math.log(1 - u) / lambda_param
                numbers.append(round(x, 4))
                
                # Mostrar progreso para muestras grandes
                if n > 50000 and i % 10000 == 0:
                    progress = (i / n) * 100
                    print(f"Progreso: {progress:.1f}%")
                    
        except Exception as e:
            raise Exception(f"Error generando distribución exponencial: {str(e)}")
            
        return numbers
    
    def generate_normal(self, n, mu, sigma):
        """Genera números aleatorios con distribución normal usando Box-Muller
        
        El método Box-Muller transforma dos variables uniformes independientes
        en dos variables normales estándar independientes:
        Z0 = √(-2ln(U1)) * cos(2πU2)
        Z1 = √(-2ln(U1)) * sin(2πU2)
        Luego: X = μ + σ*Z
        """
        numbers = []
        try:
            i = 0
            while i < n:
                # Box-Muller transform
                u1 = random.random()
                u2 = random.random()
                
                # Evitar log(0)
                while u1 == 0:
                    u1 = random.random()
                
                z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
                z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
                
                x0 = mu + sigma * z0
                x1 = mu + sigma * z1
                
                numbers.append(round(x0, 4))
                i += 1
                
                if i < n:
                    numbers.append(round(x1, 4))
                    i += 1
                
                # Mostrar progreso para muestras grandes
                if n > 50000 and i % 10000 == 0:
                    progress = (i / n) * 100
                    print(f"Progreso: {progress:.1f}%")
                    
        except Exception as e:
            raise Exception(f"Error generando distribución normal: {str(e)}")
                
        return numbers[:n]
    
    def update_data_display(self):
        """Actualiza la visualización de los datos generados"""
        try:
            self.data_text.delete(1.0, tk.END)
            
            if not self.generated_numbers:
                self.data_text.insert(1.0, "No hay datos generados")
                return
            
            # Mostrar los números en formato de columnas
            data_str = ""
            numbers_per_row = 10
            
            # Agregar encabezado con información
            header = f"Datos generados - {self.generation_parameters.get('distribución', 'N/A')}\n"
            header += f"Muestra: {len(self.generated_numbers):,} números\n"
            header += f"Fecha: {self.generation_parameters.get('fecha_generación', 'N/A')}\n"
            header += "-" * 80 + "\n\n"
            data_str += header
            
            # Agregar números en formato tabular
            for i, num in enumerate(self.generated_numbers):
                data_str += f"{num:8.4f}\t"
                if (i + 1) % numbers_per_row == 0:  # Nueva línea cada 10 números
                    data_str += "\n"
            
            # Si no termina en nueva línea, agregarla
            if len(self.generated_numbers) % numbers_per_row != 0:
                data_str += "\n"
                
            # Agregar estadísticas al final para muestras pequeñas
            if len(self.generated_numbers) <= 1000:
                data_str += f"\n{'-' * 80}\n"
                data_str += f"Estadísticas rápidas:\n"
                data_str += f"Media: {np.mean(self.generated_numbers):.4f}\n"
                data_str += f"Desv. Est.: {np.std(self.generated_numbers, ddof=1):.4f}\n"
                data_str += f"Mínimo: {min(self.generated_numbers):.4f}\n"
                data_str += f"Máximo: {max(self.generated_numbers):.4f}"
            
            self.data_text.insert(1.0, data_str)
            
        except Exception as e:
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(1.0, f"Error al mostrar datos: {str(e)}")
            print(f"Error en update_data_display: {e}")
    
    def update_histogram(self):
        """Actualiza el histograma con validaciones mejoradas"""
        try:
            # Limpiar frame anterior
            for widget in self.histogram_canvas_frame.winfo_children():
                widget.destroy()
                
            if not self.generated_numbers:
                # Mostrar mensaje cuando no hay datos
                no_data_label = ttk.Label(self.histogram_canvas_frame, 
                                        text="No hay datos para mostrar.\nGenere números primero.",
                                        font=("Arial", 12))
                no_data_label.pack(expand=True)
                return
                
            # Verificar que hay suficientes datos para el histograma
            if len(self.generated_numbers) < 5:
                warning_label = ttk.Label(self.histogram_canvas_frame,
                                        text="Se necesitan al menos 5 números para generar un histograma significativo.",
                                        font=("Arial", 10))
                warning_label.pack(expand=True)
                return
                
            # Crear figura con tamaño apropiado
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Número de intervalos
            n_intervals = int(self.intervals_var.get())
            
            # Verificar que hay suficientes datos para el número de intervalos
            if len(self.generated_numbers) < n_intervals:
                n_intervals = max(1, len(self.generated_numbers) // 2)
                messagebox.showwarning("Advertencia", 
                                     f"Muy pocos datos para {self.intervals_var.get()} intervalos. "
                                     f"Usando {n_intervals} intervalos.")
            
            # Crear histograma
            counts, bins, patches = ax.hist(self.generated_numbers, bins=n_intervals, 
                                          edgecolor='black', alpha=0.7, color='skyblue',
                                          density=False)
            
            # Configurar etiquetas y título
            distribution = self.generation_parameters.get('distribución', 'Desconocida')
            title = f'Histograma - Distribución {distribution}\n'
            title += f'({len(self.generated_numbers):,} números, {n_intervals} intervalos)'
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.set_xlabel('Valor', fontsize=12)
            ax.set_ylabel('Frecuencia', fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # Añadir estadísticas
            mean_val = np.mean(self.generated_numbers)
            std_val = np.std(self.generated_numbers, ddof=1)
            min_val = min(self.generated_numbers)
            max_val = max(self.generated_numbers)
            
            stats_text = f'Media: {mean_val:.4f}\n'
            stats_text += f'Desv. Est.: {std_val:.4f}\n'
            stats_text += f'Rango: [{min_val:.4f}, {max_val:.4f}]'
            
            ax.text(0.02, 0.98, stats_text, 
                    transform=ax.transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                    fontsize=10)
            
            # Mejorar el formato de los ejes
            ax.ticklabel_format(style='plain', useOffset=False)
            
            plt.tight_layout()
            
            # Integrar en tkinter
            canvas = FigureCanvasTkAgg(fig, self.histogram_canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            # Mostrar error en el frame del histograma
            for widget in self.histogram_canvas_frame.winfo_children():
                widget.destroy()
            error_label = ttk.Label(self.histogram_canvas_frame,
                                  text=f"Error al generar histograma:\n{str(e)}",
                                  font=("Arial", 10))
            error_label.pack(expand=True)
            print(f"Error en update_histogram: {e}")
            import traceback
            traceback.print_exc()
    
    def update_frequency_table(self):
        """Actualiza la tabla de frecuencias con validaciones mejoradas"""
        try:
            # Limpiar tabla anterior
            for item in self.freq_tree.get_children():
                self.freq_tree.delete(item)
                
            if not self.generated_numbers:
                # Insertar mensaje cuando no hay datos
                self.freq_tree.insert("", "end", values=(
                    "No hay datos", "", "", "", "", ""
                ))
                return
                
            # Verificar cantidad mínima de datos
            if len(self.generated_numbers) < 2:
                self.freq_tree.insert("", "end", values=(
                    "Datos insuficientes", "", "", "", "", ""
                ))
                return
                
            # Calcular intervalos y frecuencias
            n_intervals = int(self.intervals_var.get())
            min_val = min(self.generated_numbers)
            max_val = max(self.generated_numbers)
            
            # Verificar que hay variación en los datos
            if min_val == max_val:
                self.freq_tree.insert("", "end", values=(
                    f"[{min_val:.4f}]", f"{min_val:.4f}", f"{max_val:.4f}", 
                    len(self.generated_numbers), "1.0000", len(self.generated_numbers)
                ))
                self.frequency_table = [{
                    'Intervalo': f"[{min_val:.4f}]",
                    'Límite Inf': f"{min_val:.4f}",
                    'Límite Sup': f"{max_val:.4f}",
                    'Frecuencia': len(self.generated_numbers),
                    'Freq. Relativa': "1.0000",
                    'Freq. Acumulada': len(self.generated_numbers)
                }]
                return
            
            # Ajustar número de intervalos si hay pocos datos
            if len(self.generated_numbers) < n_intervals:
                n_intervals = max(1, len(self.generated_numbers) // 2)
            
            # Crear intervalos con un pequeño ajuste para evitar problemas de precisión
            epsilon = (max_val - min_val) * 1e-10
            interval_width = (max_val - min_val + epsilon) / n_intervals
            bins = [min_val + i * interval_width for i in range(n_intervals + 1)]
            bins[-1] = max_val  # Asegurar que el último bin incluya el valor máximo
            
            # Calcular frecuencias
            frequencies = [0] * n_intervals
            for num in self.generated_numbers:
                # Encontrar el intervalo correspondiente
                if num == max_val:
                    # El valor máximo va en el último intervalo
                    interval_idx = n_intervals - 1
                else:
                    interval_idx = min(int((num - min_val) / interval_width), n_intervals - 1)
                frequencies[interval_idx] += 1
            
            # Crear tabla de frecuencias
            total = len(self.generated_numbers)
            cumulative_freq = 0
            
            self.frequency_table = []
            
            for i in range(n_intervals):
                freq = frequencies[i]
                rel_freq = freq / total if total > 0 else 0
                cumulative_freq += freq
                cum_rel_freq = cumulative_freq / total if total > 0 else 0
                
                # Formato del intervalo
                interval_str = f"[{bins[i]:.4f}, {bins[i+1]:.4f})"
                if i == n_intervals - 1:  # Último intervalo cerrado
                    interval_str = f"[{bins[i]:.4f}, {bins[i+1]:.4f}]"
                
                row_data = {
                    'Intervalo': interval_str,
                    'Límite Inf': f"{bins[i]:.4f}",
                    'Límite Sup': f"{bins[i+1]:.4f}",
                    'Frecuencia': freq,
                    'Freq. Relativa': f"{rel_freq:.4f}",
                    'Freq. Acumulada': cumulative_freq
                }
                
                self.frequency_table.append(row_data)
                
                # Insertar en treeview con formato condicional
                tag = "even" if i % 2 == 0 else "odd"
                if freq == 0:
                    tag = "empty"
                    
                self.freq_tree.insert("", "end", values=(
                    interval_str,
                    f"{bins[i]:.4f}",
                    f"{bins[i+1]:.4f}",
                    freq,
                    f"{rel_freq:.4f}",
                    cumulative_freq
                ), tags=(tag,))
            
            # Configurar colores alternados para mejor legibilidad
            self.freq_tree.tag_configure("even", background="#f0f0f0")
            self.freq_tree.tag_configure("odd", background="white")
            self.freq_tree.tag_configure("empty", background="#ffeeee")
            
            # Verificación de integridad
            total_freq = sum(frequencies)
            if total_freq != total:
                print(f"Advertencia: Total de frecuencias ({total_freq}) no coincide con total de datos ({total})")
                
        except Exception as e:
            # Limpiar y mostrar error
            for item in self.freq_tree.get_children():
                self.freq_tree.delete(item)
            self.freq_tree.insert("", "end", values=(
                f"Error: {str(e)}", "", "", "", "", ""
            ))
            print(f"Error en update_frequency_table: {e}")
            import traceback
            traceback.print_exc()
    
    def copy_data(self):
        """Copia los datos generados al portapapeles con validaciones mejoradas"""
        if not self.generated_numbers:
            messagebox.showwarning("Advertencia", "No hay datos para copiar")
            return
            
        try:
            # Verificar tamaño de datos para advertir sobre rendimiento
            if len(self.generated_numbers) > 100000:
                result = messagebox.askyesno("Datos Grandes", 
                                           f"Está a punto de copiar {len(self.generated_numbers):,} números.\n"
                                           f"Esto puede tardar un momento y usar mucha memoria.\n\n"
                                           f"¿Desea continuar?")
                if not result:
                    return
            
            # Crear string con los datos
            if len(self.generated_numbers) <= 10000:
                # Para conjuntos pequeños, agregar encabezado
                header = f"# Datos generados - {self.generation_parameters.get('distribución', 'N/A')}\n"
                header += f"# Muestra: {len(self.generated_numbers):,} números\n"
                header += f"# Fecha: {self.generation_parameters.get('fecha_generación', 'N/A')}\n"
                header += f"# Valor\n"
                data_str = header + "\n".join([f"{num:.4f}" for num in self.generated_numbers])
            else:
                # Para conjuntos grandes, solo los números
                data_str = "\n".join([f"{num:.4f}" for num in self.generated_numbers])
            
            # Copiar al portapapeles
            self.root.clipboard_clear()
            self.root.clipboard_append(data_str)
            
            # Mensaje de éxito
            success_msg = f"¡Datos copiados exitosamente!\n\n"
            success_msg += f"Números copiados: {len(self.generated_numbers):,}\n"
            success_msg += f"Tamaño aproximado: {len(data_str)} caracteres\n\n"
            success_msg += f"Los datos están listos para pegar en cualquier aplicación."
            
            messagebox.showinfo("Copia Exitosa", success_msg)
            
        except MemoryError:
            messagebox.showerror("Error de Memoria", 
                               "No hay suficiente memoria para copiar todos los datos.\n"
                               "Intente exportar a Excel en su lugar.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al copiar datos: {str(e)}")
            print(f"Error en copy_data: {e}")
    
    def copy_frequency_table(self):
        """Copia la tabla de frecuencias al portapapeles"""
        if not self.frequency_table:
            messagebox.showwarning("Advertencia", "No hay tabla de frecuencias para copiar")
            return
            
        try:
            # Crear formato CSV
            header = "Intervalo\tLímite Inf\tLímite Sup\tFrecuencia\tFreq. Relativa\tFreq. Acumulada\n"
            rows = []
            
            for row in self.frequency_table:
                row_str = f"{row['Intervalo']}\t{row['Límite Inf']}\t{row['Límite Sup']}\t{row['Frecuencia']}\t{row['Freq. Relativa']}\t{row['Freq. Acumulada']}"
                rows.append(row_str)
            
            table_str = header + "\n".join(rows)
            
            self.root.clipboard_clear()
            self.root.clipboard_append(table_str)
            messagebox.showinfo("Éxito", "Tabla de frecuencias copiada al portapapeles")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al copiar tabla: {str(e)}")
    
    def export_to_excel(self):
        """Exporta los datos y análisis a un archivo Excel"""
        if not self.generated_numbers:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
            
        try:
            # Crear nombre de archivo por defecto
            default_filename = f"datos_aleatorios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Solicitar ubicación del archivo
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")],
                title="Guardar datos como Excel",
                initialfile=default_filename
            )
            
            if not file_path:
                return
            
            # Verificar que el archivo tenga extensión .xlsx
            if not file_path.lower().endswith('.xlsx'):
                file_path += '.xlsx'
            
            # Crear el archivo Excel con pandas
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                
                # Hoja 1: Números generados
                df_numbers = pd.DataFrame({
                    'Número': range(1, len(self.generated_numbers) + 1),
                    'Valor': self.generated_numbers
                })
                df_numbers.to_excel(writer, sheet_name='Números Generados', index=False)
                
                # Hoja 2: Tabla de frecuencias
                if self.frequency_table:
                    df_freq = pd.DataFrame(self.frequency_table)
                    df_freq.to_excel(writer, sheet_name='Tabla de Frecuencias', index=False)
                
                # Hoja 3: Resumen estadístico
                stats_data = {
                    'Estadística': [
                        'Distribución',
                        'Tamaño de muestra',
                        'Fecha de generación',
                        'Intervalos utilizados',
                        'Media observada',
                        'Desviación estándar observada',
                        'Valor mínimo',
                        'Valor máximo',
                        'Mediana',
                        'Primer cuartil (Q1)',
                        'Tercer cuartil (Q3)'
                    ],
                    'Valor': [
                        self.generation_parameters.get('distribución', 'N/A'),
                        self.generation_parameters.get('tamaño_muestra', 'N/A'),
                        self.generation_parameters.get('fecha_generación', 'N/A'),
                        self.generation_parameters.get('intervalos', 'N/A'),
                        f"{np.mean(self.generated_numbers):.4f}",
                        f"{np.std(self.generated_numbers, ddof=1):.4f}",
                        f"{min(self.generated_numbers):.4f}",
                        f"{max(self.generated_numbers):.4f}",
                        f"{np.median(self.generated_numbers):.4f}",
                        f"{np.percentile(self.generated_numbers, 25):.4f}",
                        f"{np.percentile(self.generated_numbers, 75):.4f}"
                    ]
                }
                
                # Agregar parámetros específicos de la distribución
                distribution = self.generation_parameters.get('distribución', '')
                if distribution == 'Uniforme':
                    stats_data['Estadística'].extend(['Parámetro a (límite inf)', 'Parámetro b (límite sup)'])
                    stats_data['Valor'].extend([
                        str(self.generation_parameters.get('a', 'N/A')),
                        str(self.generation_parameters.get('b', 'N/A'))
                    ])
                elif distribution == 'Exponencial':
                    stats_data['Estadística'].append('Parámetro λ (lambda)')
                    stats_data['Valor'].append(str(self.generation_parameters.get('lambda', 'N/A')))
                elif distribution == 'Normal':
                    stats_data['Estadística'].extend(['Parámetro μ (media)', 'Parámetro σ (desv. est.)'])
                    stats_data['Valor'].extend([
                        str(self.generation_parameters.get('mu', 'N/A')),
                        str(self.generation_parameters.get('sigma', 'N/A'))
                    ])
                
                df_stats = pd.DataFrame(stats_data)
                df_stats.to_excel(writer, sheet_name='Resumen Estadístico', index=False)
                
                # Hoja 4: Información del sistema
                system_info = {
                    'Información': [
                        'Sistema Operativo',
                        'Versión de Python',
                        'Memoria RAM total (GB)',
                        'Memoria RAM disponible (GB)',
                        'Archivo generado por',
                        'Fecha de exportación'
                    ],
                    'Detalle': [
                        f"{os.name} - {sys.platform}",
                        sys.version.split()[0],
                        f"{psutil.virtual_memory().total / (1024**3):.2f}",
                        f"{psutil.virtual_memory().available / (1024**3):.2f}",
                        "Generador de Números Aleatorios - TP2 Simulación",
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ]
                }
                df_system = pd.DataFrame(system_info)
                df_system.to_excel(writer, sheet_name='Información del Sistema', index=False)
            
            # Verificar que el archivo se creó correctamente
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                messagebox.showinfo("Exportación Exitosa", 
                                  f"¡Datos exportados exitosamente!\n\n"
                                  f"Archivo: {os.path.basename(file_path)}\n"
                                  f"Ubicación: {os.path.dirname(file_path)}\n"
                                  f"Tamaño: {file_size:,} bytes\n\n"
                                  f"El archivo contiene 4 hojas:\n"
                                  f"• Números Generados ({len(self.generated_numbers):,} números)\n"
                                  f"• Tabla de Frecuencias\n"
                                  f"• Resumen Estadístico\n"
                                  f"• Información del Sistema")
            else:
                messagebox.showerror("Error", "El archivo no se creó correctamente")
            
        except PermissionError:
            messagebox.showerror("Error de Permisos", 
                               "No se puede escribir en el archivo seleccionado.\n\n"
                               "Posibles causas:\n"
                               "• El archivo está abierto en Excel u otra aplicación\n"
                               "• No tienes permisos de escritura en la carpeta\n"
                               "• El archivo está protegido contra escritura\n\n"
                               "Solución: Cierra el archivo si está abierto e intenta de nuevo.")
        except FileNotFoundError:
            messagebox.showerror("Error de Archivo", 
                               "No se pudo crear el archivo en la ubicación especificada.\n"
                               "Verifica que la carpeta existe y tienes permisos.")
        except Exception as e:
            messagebox.showerror("Error de Exportación", 
                               f"Error inesperado al exportar a Excel:\n\n"
                               f"Error: {str(e)}\n\n"
                               f"Si el problema persiste, intenta:\n"
                               f"• Cambiar la ubicación del archivo\n"
                               f"• Verificar permisos de la carpeta\n"
                               f"• Cerrar Excel si está abierto")
            print(f"Error detallado en export_to_excel: {e}")
            import traceback
            traceback.print_exc()

def main():
    root = tk.Tk()
    app = RandomNumberGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()