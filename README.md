# 💰 Dashboard de Finanzas Personales con Streamlit

Este repositorio aloja una aplicación interactiva desarrollada con **Streamlit** para el análisis experto de finanzas personales. Su objetivo es transformar datos brutos de movimientos bancarios y saldos de cuentas en **Indicadores Clave de Rendimiento (KPIs)** y visualizaciones accionables, permitiendo una toma de decisiones financiera informada.

## 🚀 Características Clave del Dashboard

El diseño del dashboard se basa en la jerarquía visual y la usabilidad, proporcionando información esencial de un vistazo:

### 1. Indicadores Clave (KPIs)

Sección de cabecera con métricas críticas para la salud financiera:

* **Saldo Total Actual:** La liquidez total en un solo número.
* **Ingresos:** Ingresos en el período seleccionado. El indicador muestra ingresos fijos, sin extras.
* **Gastos:** Gastos en el período seleccionado.
* **Tasa de Ahorro/Gasto:** El porcentaje de ingresos que se está ahorrando o gastando de más.

### 2. Análisis de Tendencia

* **Evolución Temporal de Ingresos vs. Gastos:** Gráfico de líneas que compara la dinámica del flujo de caja a lo largo del tiempo.
* **Distribución de Gastos por Categoría:** Gráfico de tarta/donut para visualizar dónde se concentra el gasto (Vivienda, Ocio, Alimentación, etc.).

### 3. Seguimiento de Cuentas

* **Distribución de Capital:** Visualización de la distribución del saldo total entre las diferentes cuentas bancarias.
* **Detalle de Cuentas:** Tabla que muestra Saldo Inicial, Saldo Final y Movimiento Neto por cuenta.

### 4. Herramientas de Interacción (Sidebar)

Todos los gráficos son dinámicos y se actualizan con los filtros disponibles en la barra lateral:

* **Selector de Rango de Fechas:** Filtro principal para seleccionar el período de análisis.

## 📊 Estructura del Layout (Diseño Streamlit)

El diseño utiliza las funciones de Streamlit para una presentación óptima:

| Sección | Componentes Streamlit | Finalidad |
| :--- | :--- | :--- |
| **Filter Panel** | `st.sidebar` (Selectores, Rango de Fechas) | Control y Filtros Globales |
| **Cabecera** | `st.columns(4)` con `st.metric` | Resumen inmediato y KPIs críticos |
| **Zona Principal 1** | Gráfico de Líneas (Ancho Completo) | Análisis de Tendencia de Flujo de Caja |
| **Zona Principal 2** | `st.columns(2)` (Gráfico de Tarta + Tabla de Saldos) | Desglose Detallado de Gastos y Liquidez |

## 🛠️ Requisitos de Datos

La aplicación está diseñada para consumir datos desde dos hojas de un archivo Excel (o archivos CSV):

1.  **Hoja de Movimientos (`movimientos`)**:
    * `fecha` (Date)
    * `importe` (Float)
    * `categoria del gasto` (String)
    * `cuenta` (String)
2.  **Hoja de Cuentas (`cuentas`)**:
    * `cuenta` (String)
    * `saldo inicial` (Float)
    * `saldo final` (Float - Calculado o proveniente de la data)

## 💻 Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [URL_DE_TU_REPO]
    cd [nombre_del_repo]
    ```
2.  **Crear el entorno virtual e instalar dependencias:**
    ```bash
    # Se asume que tienes un archivo requirements.txt con: streamlit, pandas, plotly
    pip install -r requirements.txt
    ```
3.  **Asegúrate de que tus datos están cargados** (ej. en el archivo `gastos.xlsx` o similar, según la ruta que uses en tu código).
4.  **Ejecutar la aplicación Streamlit:**
    ```bash
    streamlit run app.py
    ```

El dashboard se abrirá automáticamente en tu navegador predeterminado.