# 📊 Dashboard Financiero - Análisis de AUMs

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## 🎯 Descripción del Proyecto

Dashboard interactivo profesional para el análisis de **Assets Under Management (AUMs)** de una entidad financiera. El proyecto procesa más de **5 millones de registros** históricos (2017-2022) para proporcionar insights accionables sobre la gestión de cartera, rendimiento de asesores y tendencias del mercado.
Este proyecto utiliza datos completamente simulados y fue desarrollado con fines académicos y demostrativos.
No contiene información real de ninguna entidad financiera.

### 🌟 Características Principales

- **📈 Análisis de Big Data**: Procesamiento eficiente de +5M registros con optimización de memoria
- **🎨 Visualizaciones Interactivas**: Gráficos dinámicos con Plotly para exploración de datos
- **🔍 Filtros Avanzados**: Segmentación por año, mes, segmento, mesa y asesor
- **📊 KPIs en Tiempo Real**: Métricas clave de negocio actualizadas dinámicamente
- **📉 Análisis de Tendencias**: Evolución temporal de AUMs y base de clientes
- **🏆 Rankings**: Top asesores y segmentos por rendimiento
- **💾 Exportación de Datos**: Descarga de reportes en CSV y Excel
- **🎯 Análisis de Retención**: Seguimiento de la evolución de la base de clientes

## 🛠️ Stack Tecnológico

```
Python 3.12+
├── Streamlit       # Framework web interactivo
├── Pandas          # Manipulación y análisis de datos
├── NumPy           # Cálculos numéricos optimizados
├── Plotly          # Visualizaciones interactivas
└── OpenPyXL        # Lectura/escritura de archivos Excel
```

## 📁 Estructura del Proyecto

```
Dashboard-Financiero/
│
├── Dashboard.py              # Aplicación principal de Streamlit
├── requirements.txt          # Dependencias del proyecto
├── README.md                # Documentación
├── AUMs_Clientes.xlsx       # Datos históricos (2017-2022)
│
├── screenshots/             # Capturas de pantalla del dashboard
│   ├── dashboard_main.png
│   ├── filters.png
│   └── charts.png
│
└── docs/                    # Documentación adicional
    └── analisis_datos.md    # Metodología de análisis
```

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.12 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio** (o descargar los archivos)

```bash
git clone https://github.com/AlvarinoAeaM/dashboard-financiero-aums.git
cd dashboard-financiero-aums
```

2. **Crear entorno virtual** (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**

```bash
streamlit run Dashboard.py
```

5. **Abrir en el navegador**

La aplicación se abrirá automáticamente en `http://localhost:8501`

## 📊 Estructura de Datos

### Archivo de Entrada: `AUMs_Clientes.xlsx`

El archivo contiene 6 hojas (una por año: 2017-2022) con las siguientes columnas:

| Columna | Descripción | Tipo |
|---------|-------------|------|
| Año | Año del registro | Integer |
| Numero de Mes | Mes del registro (1-12) | Integer |
| Segmento Mesa | Segmento de negocio | String |
| Doc. Identificación | ID del asesor | String |
| Asesor Comercial | Nombre del asesor | String |
| Mesa | Unidad de negocio | String |
| Numero Identificación | ID del cliente | String |
| Nombre Cliente | Nombre del cliente | String |
| Segmento Largo | Clasificación del cliente | String |
| AUM Fin de Mes | Assets Under Management | Float |
| No.Clientes | Cantidad de clientes | Integer |
| Segmento Cliente | Segmento básico | String |

### Volumen de Datos

- **Total de registros**: +5,200,000
- **Período**: Enero 2017 - Diciembre 2022 (72 meses)
- **Clientes únicos**: ~150,000
- **Asesores únicos**: ~800
- **Tamaño del archivo**: ~400 MB

## 📈 Funcionalidades del Dashboard

### 1. Panel de KPIs
- **AUM Total**: Suma agregada de activos bajo gestión
- **Total Clientes**: Conteo de clientes únicos
- **Asesores Activos**: Número de asesores con cartera
- **AUM Promedio**: Promedio por cliente/transacción

### 2. Análisis de Crecimiento
- Evolución anual de AUMs
- Tasas de crecimiento año a año
- Comparación interanual de clientes

### 3. Análisis por Segmento
- Distribución de AUMs por segmento de negocio
- Concentración de clientes por segmento
- Performance por mesa de trabajo

### 4. Tendencias Temporales
- Series de tiempo de AUMs mensuales
- Evolución de base de clientes
- Estacionalidad y patrones

### 5. Performance de Asesores
- Ranking de top 10 asesores por AUM
- Distribución de cartera por asesor
- Productividad y eficiencia

### 6. Análisis de Retención
- Evolución de clientes únicos
- Tasa de retención año a año
- Churn rate y nuevos clientes

## 🎨 Optimizaciones Implementadas

### Rendimiento
```python
# Uso de tipos de datos optimizados
dtype={
    'Año': 'int16',          # Reduce memoria en 75%
    'Numero de Mes': 'int8',  # Reduce memoria en 87.5%
    'AUM Fin de Mes': 'float32'  # Reduce memoria en 50%
}
```

### Caché de Datos
```python
@st.cache_data(show_spinner="Cargando datos...")
def cargar_datos():
    # Los datos se cargan una vez y se cachean
    # Reduce tiempo de respuesta de 15s a <1s
```

### Procesamiento Eficiente
- Concatenación de DataFrames optimizada
- Agregaciones con Pandas vectorizado
- Filtrado lazy evaluation

## 💡 Casos de Uso

### 1. Directores Comerciales
- Monitoreo de performance de equipo de asesores
- Identificación de tendencias y oportunidades
- Análisis de concentración de riesgo

### 2. Asesores Financieros
- Seguimiento de su cartera personal
- Benchmarking vs. otros asesores
- Identificación de clientes en riesgo

### 3. Analistas de Datos
- Análisis exploratorio de datos
- Generación de reportes personalizados
- Exportación para análisis adicionales

### 4. Gerencia Ejecutiva
- KPIs estratégicos del negocio
- Evolución de AUMs y base de clientes
- Toma de decisiones basada en datos

## 🔧 Personalización

### Agregar Nuevos Gráficos

```python
# En la sección correspondiente del Dashboard.py
fig = px.scatter(
    df_filtrado,
    x='columna_x',
    y='columna_y',
    color='segmento',
    title='Tu Nuevo Gráfico'
)
st.plotly_chart(fig, use_container_width=True)
```

### Modificar Colores del Dashboard

```python
# En la sección de estilos CSS
st.markdown("""
    <style>
    .stMetric {
        background-color: #tu-color;
    }
    </style>
""", unsafe_allow_html=True)
```

### Agregar Nuevos Filtros

```python
# En la sección de sidebar
nuevo_filtro = st.sidebar.multiselect(
    "Tu Nuevo Filtro:",
    options=df['columna'].unique(),
    default=df['columna'].unique()
)
```

## 📊 Insights Generados

### Principales Hallazgos (2017-2022)

1. **Crecimiento de AUMs**: +45% acumulado en el período
2. **Segmento más rentable**: Banca Privada (60% de AUMs)
3. **Top Asesor**: Gestiona $2.5B en activos
4. **Retención de clientes**: 85% anual promedio
5. **Mejor año**: 2021 con 12% de crecimiento

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Roadmap

- [ ] Implementar predicciones con ML (Prophet/ARIMA)
- [ ] Agregar análisis de clusterización de clientes
- [ ] Dashboard móvil responsive
- [ ] Integración con APIs de datos en tiempo real
- [ ] Alertas automáticas por email
- [ ] Modo oscuro
- [ ] Exportación a PDF con ReportLab

## 🐛 Problemas Conocidos

- Carga inicial puede tomar 10-15 segundos con archivo completo
- Filtros múltiples con muchas opciones pueden ralentizar UI
- Excel de exportación limitado a 10,000 registros (limitación de memoria)

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👤 Autor

**Enrique Alvarino**
- LinkedIn: [Enrique Alvarino](https://www.linkedin.com/in/abdenago-enrique-alvarino-medina-a1882814b/)
- GitHub: [@AlvarinoAeaM](https://github.com/AlvarinoAeaM)
- Email: alvarinomedina@gmail.com

## 🙏 Agradecimientos

- Streamlit por el excelente framework
- Plotly por las visualizaciones interactivas
- Pandas por el procesamiento de datos
- La comunidad de Python por las herramientas open-source

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!

**Última actualización**: Febrero 2026
