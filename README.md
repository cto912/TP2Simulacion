# Generador de Números Aleatorios - TP2 Simulación

## Índice
1. [Descripción General](#descripción-general)
2. [Características Principales](#características-principales)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Funciones Principales](#funciones-principales)
5. [Distribuciones Implementadas](#distribuciones-implementadas)
6. [Interfaz de Usuario](#interfaz-de-usuario)
7. [Validaciones y Manejo de Errores](#validaciones-y-manejo-de-errores)
8. [Exportación de Datos](#exportación-de-datos)
9. [Instalación y Uso](#instalación-y-uso)
10. [Posibles Preguntas del Docente](#posibles-preguntas-del-docente)

## Descripción General

Este aplicativo es un generador completo de números aleatorios que implementa tres distribuciones estadísticas fundamentales: uniforme, exponencial y normal. Está desarrollado en Python utilizando una interfaz gráfica moderna con Tkinter, y proporciona herramientas avanzadas de visualización y análisis estadístico.

### Objetivos del Proyecto
- Generar secuencias de números aleatorios con precisión de 4 decimales
- Proporcionar análisis estadístico completo mediante histogramas y tablas de frecuencia
- Permitir exportación de datos para análisis posterior
- Implementar validaciones robustas para garantizar la calidad de los datos

## Características Principales

### ✅ Generación de Números Aleatorios
- **Tamaño de muestra**: Hasta 1,000,000 números
- **Precisión**: 4 decimales exactos
- **Distribuciones**: Uniforme, Exponencial, Normal
- **Método base**: Función nativa `random.random()` de Python

### ✅ Análisis Estadístico
- **Histogramas**: Con 5, 10, 15, 20 o 25 intervalos configurables
- **Tabla de frecuencias**: Absoluta, relativa y acumulada
- **Estadísticas descriptivas**: Media y desviación estándar

### ✅ Exportación de Datos
- **Formato texto**: Para números generados
- **Formato CSV**: Para tabla de frecuencias
- **Formato Excel**: Para análisis avanzado (.xlsx)

## Arquitectura del Sistema

### Estructura de Clases

```python
class RandomNumberGenerator:
    ├── __init__(self, root)                    # Constructor principal
    ├── setup_ui(self)                          # Configuración de interfaz
    ├── setup_parameters(self)                  # Configuración de parámetros
    ├── generate_numbers(self)                  # Control principal de generación
    ├── generate_uniform(self, n, a, b)         # Generador uniforme
    ├── generate_exponential(self, n, lambda)   # Generador exponencial
    ├── generate_normal(self, n, mu, sigma)     # Generador normal
    ├── update_data_display(self)               # Actualización de datos
    ├── update_histogram(self)                  # Actualización de histograma
    ├── update_frequency_table(self)            # Actualización de tabla
    ├── copy_data(self)                         # Copia de datos
    ├── copy_frequency_table(self)              # Copia de tabla
    └── export_to_excel(self)                   # Exportación a Excel
```

### Flujo de Datos

```
Entrada de Usuario → Validación → Generación → Análisis → Visualización → Exportación
```

## Funciones Principales

### 1. Constructor (`__init__`)
```python
def __init__(self, root):
```
**Propósito**: Inicializa la aplicación y configura las variables principales.

**Funcionamiento**:
- Establece el título y tamaño de la ventana principal
- Inicializa listas para almacenar datos generados
- Llama a `setup_ui()` para crear la interfaz

**Variables importantes**:
- `self.generated_numbers`: Lista que almacena los números generados
- `self.frequency_table`: Diccionario con la tabla de frecuencias

### 2. Configuración de Interfaz (`setup_ui`)
```python
def setup_ui(self):
```
**Propósito**: Crea toda la interfaz gráfica de usuario.

**Componentes creados**:
- **Frame de configuración**: Controles de entrada
- **Notebook con pestañas**: Organización de resultados
- **Widgets específicos**: Entry, Combobox, Button, etc.

**Organización visual**:
- Lado izquierdo: Configuración y parámetros
- Lado derecho: Resultados en pestañas

### 3. Generadores de Distribuciones

#### 3.1 Distribución Uniforme (`generate_uniform`)
```python
def generate_uniform(self, n, a, b):
```
**Algoritmo implementado**:
1. Genera `u` uniformemente en [0,1] usando `random.random()`
2. Aplica transformación lineal: `x = a + (b-a) * u`
3. Redondea a 4 decimales

**Fundamento matemático**:
- Si U ~ Uniforme(0,1), entonces X = a + (b-a)U ~ Uniforme(a,b)

#### 3.2 Distribución Exponencial (`generate_exponential`)
```python
def generate_exponential(self, n, lambda_param):
```
**Algoritmo implementado**:
1. Genera `u` uniformemente en [0,1]
2. Aplica transformación inversa: `x = -ln(1-u) / λ`
3. Redondea a 4 decimales

**Fundamento matemático**:
- Método de transformación inversa usando F⁻¹(u) = -ln(1-u)/λ
- Donde F(x) = 1 - e^(-λx) es la CDF exponencial

#### 3.3 Distribución Normal (`generate_normal`)
```python
def generate_normal(self, n, mu, sigma):
```
**Algoritmo implementado**: Box-Muller Transform
1. Genera dos números uniformes independientes u₁, u₂
2. Calcula:
   - z₀ = √(-2ln(u₁)) * cos(2πu₂)
   - z₁ = √(-2ln(u₁)) * sin(2πu₂)
3. Transforma: x = μ + σz

**Fundamento matemático**:
- Genera dos variables normales estándar independientes
- Aplica transformación lineal para obtener N(μ,σ²)

### 4. Análisis Estadístico

#### 4.1 Actualización de Histograma (`update_histogram`)
```python
def update_histogram(self):
```
**Funcionamiento**:
1. Calcula intervalos óptimos según el número especificado
2. Genera histograma usando `matplotlib.pyplot.hist()`
3. Añade estadísticas descriptivas (media, desviación estándar)
4. Configura etiquetas, títulos y formato

**Elementos visuales**:
- Barras con borde negro y relleno azul claro
- Grilla de fondo para mejor lectura
- Cuadro de estadísticas en la esquina superior izquierda

#### 4.2 Tabla de Frecuencias (`update_frequency_table`)
```python
def update_frequency_table(self):
```
**Proceso de cálculo**:
1. **Determinación de intervalos**:
   - Rango: [min, max] de los datos
   - Ancho de intervalo: (max - min) / número_intervalos
   
2. **Cálculo de frecuencias**:
   - Frecuencia absoluta: conteo en cada intervalo
   - Frecuencia relativa: frecuencia / total
   - Frecuencia acumulada: suma progresiva

3. **Formato de presentación**:
   - Intervalos cerrados a la izquierda: [a, b)
   - Último intervalo cerrado en ambos extremos: [a, b]

## Distribuciones Implementadas

### 1. Distribución Uniforme Continua

**Definición**: Una variable aleatoria X tiene distribución uniforme en [a,b] si todos los valores en el intervalo tienen la misma probabilidad.

**Función de densidad**:
```
f(x) = 1/(b-a)  para a ≤ x ≤ b
f(x) = 0        en otro caso
```

**Parámetros**:
- `a`: Límite inferior
- `b`: Límite superior (debe ser > a)

**Aplicaciones**:
- Simulación de eventos equiprobables
- Generación de números base para otras distribuciones

### 2. Distribución Exponencial

**Definición**: Modela el tiempo entre eventos en un proceso de Poisson.

**Función de densidad**:
```
f(x) = λe^(-λx)  para x ≥ 0
f(x) = 0         para x < 0
```

**Parámetros**:
- `λ` (lambda): Tasa de ocurrencia (debe ser > 0)

**Propiedades**:
- Media: 1/λ
- Varianza: 1/λ²
- Propiedad de falta de memoria

**Aplicaciones**:
- Tiempos de falla de componentes
- Intervalos entre llegadas de clientes

### 3. Distribución Normal (Gaussiana)

**Definición**: La distribución continua más importante en estadística.

**Función de densidad**:
```
f(x) = (1/(σ√(2π))) * e^(-(x-μ)²/(2σ²))
```

**Parámetros**:
- `μ` (mu): Media (puede ser cualquier real)
- `σ` (sigma): Desviación estándar (debe ser > 0)

**Propiedades**:
- Simétrica alrededor de μ
- Forma de campana
- Regla 68-95-99.7

**Aplicaciones**:
- Modelado de errores de medición
- Características físicas de poblaciones
- Base del Teorema Central del Límite

## Interfaz de Usuario

### Diseño de la Interfaz

La interfaz utiliza el patrón **Master-Detail**:
- **Master**: Panel de configuración (izquierda)
- **Detail**: Panel de resultados con pestañas (derecha)

### Componentes Principales

#### 1. Panel de Configuración
- **Entry para tamaño de muestra**: Acepta valores de 1 a 1,000,000
- **Combobox de distribución**: Selección entre las tres distribuciones
- **Frame dinámico de parámetros**: Cambia según la distribución seleccionada
- **Combobox de intervalos**: 5, 10, 15, 20, 25 opciones
- **Botón generar**: Inicia el proceso de generación

#### 2. Panel de Resultados (Notebook)

**Pestaña 1: Datos Generados**
- ScrolledText con los números en formato tabular
- 10 números por fila para mejor visualización
- Botón "Copiar Datos" para exportación

**Pestaña 2: Histograma**
- Gráfico matplotlib integrado
- Configuración automática de escalas
- Estadísticas descriptivas incorporadas

**Pestaña 3: Tabla de Frecuencias**
- Treeview con columnas ordenadas
- Scrollbar vertical para tablas grandes
- Botones de copia y exportación

## Validaciones y Manejo de Errores

### Sistema de Validación en Capas

#### 1. Validación de Entrada de Datos
```python
# Validación de tamaño de muestra
if sample_size <= 0 or sample_size > 1000000:
    messagebox.showerror("Error", "El tamaño de muestra debe estar entre 1 y 1,000,000")
```

#### 2. Validación de Parámetros por Distribución

**Uniforme**:
- `a < b`: El límite inferior debe ser menor que el superior
- Ambos parámetros deben ser números válidos

**Exponencial**:
- `λ > 0`: Lambda debe ser positivo
- Verificación de formato numérico

**Normal**:
- `σ > 0`: Desviación estándar debe ser positiva
- μ puede ser cualquier número real

#### 3. Manejo de Excepciones
```python
try:
    # Operaciones principales
except ValueError as e:
    messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")
except Exception as e:
    messagebox.showerror("Error", f"Error inesperado: {str(e)}")
```

#### 4. Validaciones Adicionales Implementadas
- **Verificación de memoria**: Para muestras muy grandes
- **Validación de formato decimal**: Asegura 4 decimales exactos
- **Verificación de estado**: Antes de operaciones de copia/exportación
- **Validación de permisos**: Para operaciones de archivo

## Exportación de Datos

### 1. Copia al Portapapeles

**Datos Generados**:
```python
def copy_data(self):
    data_str = "\n".join([f"{num:.4f}" for num in self.generated_numbers])
    self.root.clipboard_clear()
    self.root.clipboard_append(data_str)
```

**Tabla de Frecuencias**:
```python
def copy_frequency_table(self):
    # Formato CSV con separadores de tabulación
    header = "Intervalo\tLímite Inf\tLímite Sup\t..."
```

### 2. Exportación a Excel (.xlsx)

La nueva funcionalidad permite exportar:
- **Hoja 1**: Números generados
- **Hoja 2**: Tabla de frecuencias detallada
- **Hoja 3**: Estadísticas resumidas

**Características del archivo Excel**:
- Formato profesional con encabezados
- Datos numéricos en formato correcto
- Fórmulas para verificación de cálculos

## Instalación y Uso

### Requisitos del Sistema
```
Python 3.7+
numpy >= 1.19.0
matplotlib >= 3.3.0
pandas >= 1.1.0
openpyxl >= 3.0.0
tkinter (incluido en Python estándar)
```

### Instalación de Dependencias
```bash
pip install numpy matplotlib pandas openpyxl
```

### Ejecución
```bash
python TP2SIM.py
```

### Flujo de Uso Típico
1. **Configurar parámetros** en el panel izquierdo
2. **Generar números** con el botón correspondiente
3. **Revisar datos** en la primera pestaña
4. **Analizar histograma** en la segunda pestaña
5. **Examinar frecuencias** en la tercera pestaña
6. **Exportar resultados** según necesidad

## Posibles Preguntas del Docente

### 1. **¿Por qué elegiste el método Box-Muller para la distribución normal?**

**Respuesta**: El método Box-Muller es matemáticamente exacto y eficiente. Transforma dos variables uniformes independientes en dos variables normales estándar independientes usando transformaciones trigonométricas. Es preferible a métodos aproximados como el Teorema Central del Límite porque:
- Genera valores exactamente normales (no aproximados)
- Es computacionalmente eficiente
- No tiene limitaciones en los valores extremos

### 2. **¿Cómo garantizas la calidad de los números aleatorios generados?**

**Respuesta**: 
- Uso la función nativa `random.random()` de Python que implementa el algoritmo Mersenne Twister
- Aplico transformaciones matemáticamente correctas para cada distribución
- Implemento validaciones de parámetros antes de la generación
- Redondeo consistente a 4 decimales para todos los números
- Las transformaciones preservan las propiedades estadísticas de las distribuciones

### 3. **¿Qué sucede si el usuario ingresa parámetros inválidos?**

**Respuesta**: El sistema implementa validación en múltiples capas:
- **Validación de formato**: Verifica que sean números válidos
- **Validación de rango**: Asegura que estén en rangos permitidos
- **Validación lógica**: Verifica relaciones entre parámetros (a < b, λ > 0, σ > 0)
- **Manejo de excepciones**: Captura errores inesperados
- **Mensajes claros**: Informa al usuario exactamente qué corregir

### 4. **¿Cómo calculas los intervalos para el histograma?**

**Respuesta**: 
1. Determino el rango: `max - min` de los datos generados
2. Calculo el ancho: `rango / número_de_intervalos`
3. Creo intervalos de igual ancho: `[min + i*ancho, min + (i+1)*ancho)`
4. El último intervalo es cerrado: `[a, b]` para incluir el valor máximo
5. Clasifico cada número en su intervalo correspondiente usando aritmética de enteros

### 5. **¿Por qué implementaste tres pestañas separadas?**

**Respuesta**: La separación mejora la usabilidad y organización:
- **Separación de responsabilidades**: Cada pestaña tiene un propósito específico
- **Mejor rendimiento**: Solo se actualiza la pestaña visible
- **Facilidad de uso**: El usuario puede enfocar su atención en un tipo de análisis
- **Escalabilidad**: Fácil agregar nuevos tipos de análisis

### 6. **¿Cómo manejas muestras muy grandes (cercanas a 1,000,000)?**

**Respuesta**:
- **Generación eficiente**: Uso bucles simples sin almacenamiento intermedio innecesario
- **Gestión de memoria**: Las listas se crean con tamaño conocido cuando es posible
- **Visualización adaptativa**: El histograma se ajusta automáticamente
- **Validación previa**: Verifico disponibilidad de recursos antes de generar
- **Feedback al usuario**: Muestro mensajes de progreso para operaciones largas

### 7. **¿Qué ventajas tiene tu implementación sobre usar NumPy directamente?**

**Respuesta**:
- **Control total**: Implemento los algoritmos matemáticos desde cero para entender el proceso
- **Transparencia**: Cada paso es visible y modificable
- **Precisión específica**: Control exacto sobre el redondeo a 4 decimales
- **Validación personalizada**: Manejo de errores específico para cada distribución
- **Interfaz integrada**: Todo en una aplicación cohesiva

### 8. **¿Cómo verificas que las distribuciones generadas son correctas?**

**Respuesta**:
- **Verificación visual**: El histograma debe mostrar la forma esperada de cada distribución
- **Estadísticas descriptivas**: Media y desviación estándar deben aproximarse a los valores teóricos
- **Exportación para validación**: Los datos se pueden exportar para pruebas estadísticas adicionales
- **Muestras grandes**: Con muestras de 100,000+ los resultados convergen a los valores teóricos
- **Comparación con literatura**: Los algoritmos implementados son estándar en la literatura

Esta documentación proporciona una base sólida para defender el proyecto ante cualquier pregunta técnica o conceptual que pueda hacer un docente.
