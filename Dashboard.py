"""
Dashboard Financiero - Análisis de AUMs (Assets Under Management)
Autor: Enrique Alvarino
Descripción: Dashboard interactivo para análisis de cartera de clientes y AUMs
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime
import io

# ==================== CONFIGURACIÓN DE PÁGINA ====================
st.set_page_config(
    page_title="Dashboard Financiero - AUMs",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS CSS PERSONALIZADOS ====================
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 3px solid #1f77b4;
    }
    .reportview-container .main footer {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== FUNCIONES DE CARGA Y CACHÉ ====================
@st.cache_data(show_spinner="Cargando datos... Por favor espera 🔄")
def cargar_datos():
    """Carga y consolida datos de todos los años con optimización de memoria"""
    archivo_excel = 'DataExce.xlsx'
    
    try:
        # Cargar todas las hojas de forma eficiente
        años = ['Base 2017', 'Base 2018', 'Base 2019', 'Base 2020', 'Base 2021', 'Base 2022']
        dataframes = []
        
        for año in años:
            df_temp = pd.read_excel(
                archivo_excel,
                sheet_name=año,
                dtype={
                    'Doc. Identificación': 'str',
                    'Numero  Identificación': 'str',
                    'Año': 'int16',
                    'Numero de Mes': 'int8',
                    'AUM Fin de Mes': 'float32',
                    'No.Clientes': 'int8'
                }
            )
            dataframes.append(df_temp)
        
        # Consolidar datos
        df_consolidado = pd.concat(dataframes, ignore_index=True)
        
        # Limpieza de datos
        df_consolidado = df_consolidado.fillna(0)
        
        # Crear columnas derivadas útiles
        df_consolidado['Fecha'] = pd.to_datetime(
            df_consolidado['Año'].astype(str) + '-' + 
            df_consolidado['Numero de Mes'].astype(str) + '-01'
        )
        
        # Nombre del mes
        meses_español = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        df_consolidado['Mes_Nombre'] = df_consolidado['Numero de Mes'].map(meses_español)
        
        return df_consolidado
    
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return None

@st.cache_data
def calcular_metricas(df):
    """Calcula métricas principales del negocio"""
    metricas = {
        'total_aum': df['AUM Fin de Mes'].sum(),
        'total_clientes': df['No.Clientes'].sum(),
        'num_asesores': df['Asesor Comercial'].nunique(),
        'num_segmentos': df['Segmento Mesa'].nunique(),
        'aum_promedio': df['AUM Fin de Mes'].mean(),
        'aum_mediano': df['AUM Fin de Mes'].median()
    }
    return metricas

@st.cache_data
def calcular_crecimiento(df):
    """Calcula tasas de crecimiento año a año"""
    df_anual = df.groupby('Año').agg({
        'AUM Fin de Mes': 'sum',
        'No.Clientes': 'sum'
    }).reset_index()
    
    df_anual['Crecimiento_AUM_%'] = df_anual['AUM Fin de Mes'].pct_change() * 100
    df_anual['Crecimiento_Clientes_%'] = df_anual['No.Clientes'].pct_change() * 100
    
    return df_anual

# ==================== FUNCIÓN PRINCIPAL ====================
def main():
    # Header
    st.title("📊 Dashboard Financiero - Análisis de AUMs")
    st.markdown("### Análisis Integral de Assets Under Management 2017-2022")
    
    # Cargar datos
    with st.spinner("Cargando datos del sistema..."):
        df = cargar_datos()
    
    if df is None:
        st.error("No se pudieron cargar los datos. Verifica que el archivo 'DataExce.xlsx' esté en el directorio.")
        return
    
    # ==================== SIDEBAR - FILTROS ====================
    st.sidebar.header("🎯 Filtros de Análisis")
    
    # Filtro de Año
    años_disponibles = sorted(df['Año'].unique())
    año_seleccionado = st.sidebar.multiselect(
        "Selecciona Año(s):",
        options=años_disponibles,
        default=años_disponibles
    )
    
    # Filtro de Mes
    meses_disponibles = sorted(df['Numero de Mes'].unique())
    mes_seleccionado = st.sidebar.multiselect(
        "Selecciona Mes(es):",
        options=meses_disponibles,
        default=meses_disponibles,
        format_func=lambda x: df[df['Numero de Mes']==x]['Mes_Nombre'].iloc[0] if len(df[df['Numero de Mes']==x]) > 0 else str(x)
    )
    
    # Filtro de Segmento
    segmentos_disponibles = sorted(df['Segmento Mesa'].unique())
    segmento_seleccionado = st.sidebar.multiselect(
        "Selecciona Segmento(s):",
        options=segmentos_disponibles,
        default=segmentos_disponibles
    )
    
    # Filtro de Mesa
    mesas_disponibles = sorted(df['Mesa'].unique())
    mesa_seleccionada = st.sidebar.multiselect(
        "Selecciona Mesa(s):",
        options=mesas_disponibles,
        default=mesas_disponibles
    )
    
    # Filtro de Asesor (top 20 por AUM)
    top_asesores = df.groupby('Asesor Comercial')['AUM Fin de Mes'].sum().nlargest(20).index.tolist()
    asesor_seleccionado = st.sidebar.multiselect(
        "Selecciona Asesor(es) (Top 20):",
        options=top_asesores,
        default=[]
    )
    
    # Aplicar filtros
    df_filtrado = df[
        (df['Año'].isin(año_seleccionado)) &
        (df['Numero de Mes'].isin(mes_seleccionado)) &
        (df['Segmento Mesa'].isin(segmento_seleccionado)) &
        (df['Mesa'].isin(mesa_seleccionada))
    ]
    
    if asesor_seleccionado:
        df_filtrado = df_filtrado[df_filtrado['Asesor Comercial'].isin(asesor_seleccionado)]
    
    # Información de filtros aplicados
    st.sidebar.markdown("---")
    st.sidebar.info(f"**Registros filtrados:** {len(df_filtrado):,} de {len(df):,}")
    
    # ==================== KPIs PRINCIPALES ====================
    st.markdown("---")
    st.subheader("📈 Indicadores Clave de Desempeño (KPIs)")
    
    metricas = calcular_metricas(df_filtrado)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="AUM Total",
            value=f"${metricas['total_aum']/1e9:.2f}B",
            delta="Billones de pesos"
        )
    
    with col2:
        st.metric(
            label="Total Clientes",
            value=f"{int(metricas['total_clientes']):,}",
            delta="Únicos"
        )
    
    with col3:
        st.metric(
            label="Asesores Activos",
            value=f"{metricas['num_asesores']:,}",
            delta="Únicos"
        )
    
    with col4:
        st.metric(
            label="AUM Promedio",
            value=f"${metricas['aum_promedio']/1e6:.2f}M",
            delta="Millones"
        )
    
    # ==================== ANÁLISIS DE CRECIMIENTO ====================
    st.markdown("---")
    st.subheader("📊 Análisis de Crecimiento Anual")
    
    df_crecimiento = calcular_crecimiento(df_filtrado)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de crecimiento de AUM
        fig_crecimiento_aum = go.Figure()
        fig_crecimiento_aum.add_trace(go.Bar(
            x=df_crecimiento['Año'],
            y=df_crecimiento['AUM Fin de Mes'],
            name='AUM Total',
            marker_color='lightblue',
            text=df_crecimiento['AUM Fin de Mes'].apply(lambda x: f'${x/1e9:.2f}B'),
            textposition='outside'
        ))
        
        fig_crecimiento_aum.update_layout(
            title='Evolución Anual de AUMs',
            xaxis_title='Año',
            yaxis_title='AUM (Pesos)',
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_crecimiento_aum, use_container_width=True)
    
    with col2:
        # Tasas de crecimiento
        fig_tasas = go.Figure()
        fig_tasas.add_trace(go.Scatter(
            x=df_crecimiento['Año'],
            y=df_crecimiento['Crecimiento_AUM_%'],
            mode='lines+markers+text',
            name='Crecimiento AUM',
            line=dict(color='green', width=3),
            marker=dict(size=10),
            text=df_crecimiento['Crecimiento_AUM_%'].apply(lambda x: f'{x:.1f}%' if pd.notna(x) else ''),
            textposition='top center'
        ))
        
        fig_tasas.update_layout(
            title='Tasa de Crecimiento Anual (%)',
            xaxis_title='Año',
            yaxis_title='Crecimiento (%)',
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_tasas, use_container_width=True)
    
    # ==================== ANÁLISIS POR SEGMENTO ====================
    st.markdown("---")
    st.subheader("🎯 Análisis por Segmento")
    
    df_segmento = df_filtrado.groupby('Segmento Mesa').agg({
        'AUM Fin de Mes': 'sum',
        'No.Clientes': 'sum',
        'Asesor Comercial': 'nunique'
    }).reset_index()
    df_segmento = df_segmento.sort_values('AUM Fin de Mes', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart de distribución de AUM
        fig_pie = px.pie(
            df_segmento,
            values='AUM Fin de Mes',
            names='Segmento Mesa',
            title='Distribución de AUM por Segmento',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart de clientes por segmento
        fig_bar_segmento = px.bar(
            df_segmento,
            x='Segmento Mesa',
            y='No.Clientes',
            title='Número de Clientes por Segmento',
            text='No.Clientes',
            color='No.Clientes',
            color_continuous_scale='Blues'
        )
        fig_bar_segmento.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_bar_segmento.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_bar_segmento, use_container_width=True)
    
    # ==================== ANÁLISIS TEMPORAL ====================
    st.markdown("---")
    st.subheader("📅 Tendencias Temporales")
    
    # Evolución mensual de AUM
    df_temporal = df_filtrado.groupby(['Año', 'Numero de Mes', 'Fecha']).agg({
        'AUM Fin de Mes': 'sum',
        'No.Clientes': 'sum'
    }).reset_index().sort_values('Fecha')
    
    fig_temporal = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Evolución Mensual de AUMs', 'Evolución Mensual de Clientes'),
        vertical_spacing=0.12,
        row_heights=[0.5, 0.5]
    )
    
    # AUM temporal
    fig_temporal.add_trace(
        go.Scatter(
            x=df_temporal['Fecha'],
            y=df_temporal['AUM Fin de Mes'],
            mode='lines+markers',
            name='AUM',
            line=dict(color='blue', width=2),
            marker=dict(size=6),
            fill='tonexty',
            fillcolor='rgba(0, 100, 255, 0.1)'
        ),
        row=1, col=1
    )
    
    # Clientes temporal
    fig_temporal.add_trace(
        go.Scatter(
            x=df_temporal['Fecha'],
            y=df_temporal['No.Clientes'],
            mode='lines+markers',
            name='Clientes',
            line=dict(color='green', width=2),
            marker=dict(size=6),
            fill='tonexty',
            fillcolor='rgba(0, 255, 100, 0.1)'
        ),
        row=2, col=1
    )
    
    fig_temporal.update_xaxes(title_text="Fecha", row=2, col=1)
    fig_temporal.update_yaxes(title_text="AUM (Pesos)", row=1, col=1)
    fig_temporal.update_yaxes(title_text="Número de Clientes", row=2, col=1)
    fig_temporal.update_layout(height=700, showlegend=True, hovermode='x unified')
    
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    # ==================== TOP ASESORES ====================
    st.markdown("---")
    st.subheader("🏆 Top 10 Asesores por AUM")
    
    df_top_asesores = df_filtrado.groupby('Asesor Comercial').agg({
        'AUM Fin de Mes': 'sum',
        'No.Clientes': 'sum'
    }).reset_index().sort_values('AUM Fin de Mes', ascending=False).head(10)
    
    fig_top_asesores = px.bar(
        df_top_asesores,
        y='Asesor Comercial',
        x='AUM Fin de Mes',
        orientation='h',
        title='Top 10 Asesores por AUM Gestionado',
        text='AUM Fin de Mes',
        color='AUM Fin de Mes',
        color_continuous_scale='Viridis'
    )
    fig_top_asesores.update_traces(
        texttemplate='$%{text:.2s}',
        textposition='outside'
    )
    fig_top_asesores.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_top_asesores, use_container_width=True)
    
    # ==================== ANÁLISIS DE RETENCIÓN ====================
    st.markdown("---")
    st.subheader("🔄 Análisis de Retención de Clientes")
    
    # Análisis de retención año a año
    años_completos = sorted(df_filtrado['Año'].unique())
    if len(años_completos) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Clientes por año
            df_retencion = df_filtrado.groupby('Año')['Numero  Identificación'].nunique().reset_index()
            df_retencion.columns = ['Año', 'Clientes Únicos']
            
            fig_retencion = px.line(
                df_retencion,
                x='Año',
                y='Clientes Únicos',
                markers=True,
                title='Clientes Únicos por Año',
                text='Clientes Únicos'
            )
            fig_retencion.update_traces(textposition='top center', line_color='purple')
            st.plotly_chart(fig_retencion, use_container_width=True)
        
        with col2:
            # Tasa de retención
            df_retencion['Cambio %'] = df_retencion['Clientes Únicos'].pct_change() * 100
            
            fig_cambio = go.Figure()
            fig_cambio.add_trace(go.Bar(
                x=df_retencion['Año'],
                y=df_retencion['Cambio %'],
                text=df_retencion['Cambio %'].apply(lambda x: f'{x:.1f}%' if pd.notna(x) else ''),
                textposition='outside',
                marker_color=df_retencion['Cambio %'].apply(lambda x: 'green' if x >= 0 else 'red')
            ))
            fig_cambio.update_layout(
                title='Cambio Anual en Base de Clientes (%)',
                xaxis_title='Año',
                yaxis_title='Cambio (%)',
                showlegend=False
            )
            st.plotly_chart(fig_cambio, use_container_width=True)
    
    # ==================== TABLA DE DATOS DETALLADA ====================
    st.markdown("---")
    st.subheader("📋 Datos Detallados")
    
    # Opciones de visualización
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        num_registros = st.slider(
            "Número de registros a mostrar:",
            min_value=10,
            max_value=1000,
            value=100,
            step=10
        )
    with col2:
        ordenar_por = st.selectbox(
            "Ordenar por:",
            options=['AUM Fin de Mes', 'Año', 'Asesor Comercial', 'Segmento Mesa']
        )
    with col3:
        orden = st.radio("Orden:", ['Descendente', 'Ascendente'])
    
    # Mostrar tabla
    df_mostrar = df_filtrado.sort_values(
        by=ordenar_por,
        ascending=(orden == 'Ascendente')
    ).head(num_registros)
    
    # Formatear columnas numéricas
    df_display = df_mostrar.copy()
    df_display['AUM Fin de Mes'] = df_display['AUM Fin de Mes'].apply(lambda x: f'${x:,.0f}')
    
    st.dataframe(
        df_display[[
            'Año', 'Mes_Nombre', 'Segmento Mesa', 'Mesa', 'Asesor Comercial',
            'Nombre Cliente', 'AUM Fin de Mes', 'No.Clientes'
        ]],
        use_container_width=True,
        height=400
    )
    
    # ==================== EXPORTACIÓN DE DATOS ====================
    st.markdown("---")
    st.subheader("💾 Exportar Datos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Exportar datos filtrados a CSV
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name=f'datos_filtrados_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv'
        )
    
    with col2:
        # Exportar resumen a Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_filtrado.head(10000).to_excel(writer, sheet_name='Datos', index=False)
            df_segmento.to_excel(writer, sheet_name='Por Segmento', index=False)
            df_top_asesores.to_excel(writer, sheet_name='Top Asesores', index=False)
        
        st.download_button(
            label="📥 Descargar Excel",
            data=buffer.getvalue(),
            file_name=f'reporte_completo_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    with col3:
        # Generar reporte PDF (placeholder)
        st.info("📄 Exportación a PDF disponible próximamente")
    
    # ==================== FOOTER ====================
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: gray; padding: 20px;'>
            <p><strong>Dashboard Financiero - Análisis de AUMs</strong></p>
            <p>Desarrollado con ❤️ usando Streamlit y Plotly</p>
            <p>Datos: 2017-2022 | Última actualización: {}</p>
        </div>
    """.format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)

# ==================== EJECUTAR APLICACIÓN ====================
if __name__ == "__main__":
    main()
