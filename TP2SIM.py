#TRABAJO PRACTICO N2 SIMULACION -GENERADOR DE NUMEROS RANDOM-
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import random
import math

class RandomNumberGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Números Aleatorios - TP2 Simulación")
        self.root.geometry("1200x800")
        
        # Variables para almacenar los datos generados
        self.generated_numbers = []
        self.frequency_table = None
        
        # Configurar la interfaz
        self.setup_ui()
        
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
        copy_table_btn.pack(anchor=tk.W)
    
    def generate_numbers(self):
        try:
            # Validar tamaño de muestra
            sample_size = int(self.sample_size_var.get())
            if sample_size <= 0 or sample_size > 1000000:
                messagebox.showerror("Error", "El tamaño de muestra debe estar entre 1 y 1,000,000")
                return
                
            # Obtener parámetros según la distribución
            distribution = self.distribution_var.get()
            
            if distribution == "Uniforme":
                a = float(self.param_a_var.get())
                b = float(self.param_b_var.get())
                if a >= b:
                    messagebox.showerror("Error", "El límite inferior debe ser menor que el superior")
                    return
                self.generated_numbers = self.generate_uniform(sample_size, a, b)
                
            elif distribution == "Exponencial":
                lambda_param = float(self.param_lambda_var.get())
                if lambda_param <= 0:
                    messagebox.showerror("Error", "Lambda debe ser mayor que 0")
                    return
                self.generated_numbers = self.generate_exponential(sample_size, lambda_param)
                
            elif distribution == "Normal":
                mu = float(self.param_mu_var.get())
                sigma = float(self.param_sigma_var.get())
                if sigma <= 0:
                    messagebox.showerror("Error", "La desviación estándar debe ser mayor que 0")
                    return
                self.generated_numbers = self.generate_normal(sample_size, mu, sigma)
            
            # Actualizar visualizaciones
            self.update_data_display()
            self.update_histogram()
            self.update_frequency_table()
            
            messagebox.showinfo("Éxito", f"Se generaron {sample_size} números aleatorios exitosamente")
            
        except ValueError as e:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def generate_uniform(self, n, a, b):
        """Genera números aleatorios con distribución uniforme"""
        numbers = []
        for _ in range(n):
            # Usar la función nativa del lenguaje para generar uniforme [0,1]
            u = random.random()
            # Transformar a [a,b]
            x = a + (b - a) * u
            numbers.append(round(x, 4))
        return numbers
    
    def generate_exponential(self, n, lambda_param):
        """Genera números aleatorios con distribución exponencial"""
        numbers = []
        for _ in range(n):
            u = random.random()
            # Método de transformación inversa
            x = -math.log(1 - u) / lambda_param
            numbers.append(round(x, 4))
        return numbers
    
    def generate_normal(self, n, mu, sigma):
        """Genera números aleatorios con distribución normal usando Box-Muller"""
        numbers = []
        i = 0
        while i < n:
            # Box-Muller transform
            u1 = random.random()
            u2 = random.random()
            
            z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
            
            x0 = mu + sigma * z0
            x1 = mu + sigma * z1
            
            numbers.append(round(x0, 4))
            i += 1
            
            if i < n:
                numbers.append(round(x1, 4))
                i += 1
                
        return numbers[:n]
    
    def update_data_display(self):
        """Actualiza la visualización de los datos generados"""
        self.data_text.delete(1.0, tk.END)
        
        # Mostrar los números en formato de columnas
        data_str = ""
        for i, num in enumerate(self.generated_numbers):
            data_str += f"{num:.4f}\t"
            if (i + 1) % 10 == 0:  # 10 números por fila
                data_str += "\n"
        
        self.data_text.insert(1.0, data_str)
    
    def update_histogram(self):
        """Actualiza el histograma"""
        # Limpiar frame anterior
        for widget in self.histogram_canvas_frame.winfo_children():
            widget.destroy()
            
        if not self.generated_numbers:
            return
            
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Número de intervalos
        n_intervals = int(self.intervals_var.get())
        
        # Crear histograma
        counts, bins, patches = ax.hist(self.generated_numbers, bins=n_intervals, 
                                      edgecolor='black', alpha=0.7, color='skyblue')
        
        # Configurar etiquetas y título
        distribution = self.distribution_var.get()
        ax.set_title(f'Histograma - Distribución {distribution}\n({len(self.generated_numbers)} números, {n_intervals} intervalos)')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Frecuencia')
        ax.grid(True, alpha=0.3)
        
        # Añadir estadísticas
        mean_val = np.mean(self.generated_numbers)
        std_val = np.std(self.generated_numbers)
        ax.text(0.02, 0.98, f'Media: {mean_val:.4f}\nDesv. Est.: {std_val:.4f}', 
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        
        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, self.histogram_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_frequency_table(self):
        """Actualiza la tabla de frecuencias"""
        # Limpiar tabla anterior
        for item in self.freq_tree.get_children():
            self.freq_tree.delete(item)
            
        if not self.generated_numbers:
            return
            
        # Calcular intervalos y frecuencias
        n_intervals = int(self.intervals_var.get())
        min_val = min(self.generated_numbers)
        max_val = max(self.generated_numbers)
        
        # Crear intervalos
        interval_width = (max_val - min_val) / n_intervals
        bins = [min_val + i * interval_width for i in range(n_intervals + 1)]
        
        # Calcular frecuencias
        frequencies = [0] * n_intervals
        for num in self.generated_numbers:
            # Encontrar el intervalo correspondiente
            interval_idx = min(int((num - min_val) / interval_width), n_intervals - 1)
            frequencies[interval_idx] += 1
        
        # Crear tabla de frecuencias
        total = len(self.generated_numbers)
        cumulative_freq = 0
        
        self.frequency_table = []
        
        for i in range(n_intervals):
            freq = frequencies[i]
            rel_freq = freq / total
            cumulative_freq += freq
            cum_rel_freq = cumulative_freq / total
            
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
            
            # Insertar en treeview
            self.freq_tree.insert("", "end", values=(
                interval_str,
                f"{bins[i]:.4f}",
                f"{bins[i+1]:.4f}",
                freq,
                f"{rel_freq:.4f}",
                cumulative_freq
            ))
    
    def copy_data(self):
        """Copia los datos generados al portapapeles"""
        if not self.generated_numbers:
            messagebox.showwarning("Advertencia", "No hay datos para copiar")
            return
            
        data_str = "\n".join([f"{num:.4f}" for num in self.generated_numbers])
        self.root.clipboard_clear()
        self.root.clipboard_append(data_str)
        messagebox.showinfo("Éxito", "Datos copiados al portapapeles")
    
    def copy_frequency_table(self):
        """Copia la tabla de frecuencias al portapapeles"""
        if not self.frequency_table:
            messagebox.showwarning("Advertencia", "No hay tabla de frecuencias para copiar")
            return
            
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

def main():
    root = tk.Tk()
    app = RandomNumberGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()