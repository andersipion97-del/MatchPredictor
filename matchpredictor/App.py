import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from models.predictor import (
    resumen_head_to_head, 
    obtener_partidos_equipo,
    predecir_poisson,
)
from utils.data_loader import cargar_datos
from utils.visualizations import (
    graficar_rendimiento_reciente, 
    graficar_goles_recibidos,
    graficar_radar,
    graficar_prediccion_poisson
)
from ui.styles import load_custom_css
from ui.components import scoreboard, metricas_resumen

#Definimos titulo de la aplicacion
st.set_page_config(page_title="Matchpredictor", layout="wide")

#manejo de estado para el tema
if "tema" not in st.session_state:
    st.session_state.tema = "claro"

#elegir entre tema claro y oscuro
tema = st.sidebar.radio(
    "selecciona un tema", 
    ["Claro", "Oscuro"],
    index=0 if st.session_state.tema == "Claro" else 1,
    key="tema_selector"
)

#actualizar el tema de la aplicacion
if tema != st.session_state.tema:
    st.session_state.tema = tema

#cargar estilos segun el tema seleccionado
load_custom_css(st.session_state.tema)

#definimos el titulo de la pagina
st.title("⚽ MatchPredictor")
st.markdown("Compara equipos, revisa su rendimiento y visualiza estadísticas de partidos recientes.")

#Seleccionar equipos
df_equipos, df_h2h = cargar_datos("data\partidos.xlsx")
st.sidebar.header("Configuración de Equipos")

equipos = df_equipos["Equipos"].dropna().unique().tolist()

equipo1 = st.sidebar.selectbox("Selecciona el Equipo 1", equipos)
equipo2 = st.sidebar.selectbox("Selecciona el Equipo 2", equipos)

#Validar seleccion
if equipo1 == equipo2:
    st.error("Por favor, selecciona dos equipos diferentes.")
    st.stop()

#Filtros dinamicos
st.sidebar.subheader("Filtros")
num_partidos = st.sidebar.slider(
    "Número de partidos a comparar", 
    min_value=3, 
    max_value=10, 
    value=5,
    step=1
    )

#Ultimos partidos de cada equipo
df_ultimos1 = obtener_partidos_equipo(equipo1, max_partidos=num_partidos)
df_ultimos2 = obtener_partidos_equipo(equipo2, max_partidos=num_partidos)

#cargar datos para head-to-head

#Filtrar enfretamientos entre los 2 equipos seleccionados
df_h2h = df_h2h[(df_h2h["Local"].isin([equipo1, equipo2])) &
                (df_h2h["Visitante"].isin([equipo1, equipo2]))]

#Lista de torneos únicos
torneos = df_h2h["Torneo"].dropna().unique().tolist()

#control desde la sidebar filtro por torneo
torneo_seleccionado = st.sidebar.multiselect(
    "Filtrar por torneo",
    options=torneos,
    default=torneos #selecciona todos por defecto
)

#filtro de rango de fechas
fecha_min = df_h2h["Fecha"].min()
fecha_max = df_h2h["Fecha"].max()

if pd.isna(fecha_min) or pd.isna(fecha_max):
    # Usa rango por defecto
    fecha_min = pd.Timestamp("2020-01-01")
    fecha_max = pd.Timestamp.today()

rango_fechas = st.sidebar.date_input(
    "Rango de fechas",
    value=[fecha_min, fecha_max],
    min_value=fecha_min,
    max_value=fecha_max
)

#Aplicar filtros de torneos
if torneo_seleccionado:
    df_h2h = df_h2h[df_h2h["Torneo"].isin(torneo_seleccionado)]
    
#Aplicar filtro de rango de fechas
if isinstance(rango_fechas, tuple) and len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas
    df_h2h = df_h2h[(df_h2h["Fecha"] >= pd.to_datetime(fecha_inicio)) &
                    (df_h2h["Fecha"] <= pd.to_datetime(fecha_fin))]


# Crear tabs para organizar la visualización
tab1, tab2, tab3 = st.tabs(["📊 Resumen", "⚽ Forma Reciente", "🕸️ Radar Estadísticas"])

with tab1:
    st.header("📊 Resumen del partido")
    
    scoreboard(equipo1, equipo2)
    
    resumen = resumen_head_to_head(df_h2h, equipo1, equipo2)
    metricas_resumen(resumen, equipo1, equipo2)
    
    col1, col2 = st.columns(2)
    
    # Mostrar tabla de enfrentamientos directos
    st.subheader("📅 Historial Head-to-Head")
    st.table(pd.DataFrame(resumen.items(), columns=["Estadística", "Valor"]))
    
    with col1:
        st.subheader(f"{equipo1}")
        st.metric("Victorias recientes", resumen.get(f"Victorias {equipo1}", 0))
        st.metric("Goles anotados", resumen.get(f"Goles {equipo1}", 0))

    with col2:
        st.subheader(f"{equipo2}")
        st.metric("Victorias recientes", resumen.get(f"Victorias {equipo2}", 0))
        st.metric("Goles anotados", resumen.get(f"Goles {equipo2}", 0))
    
    # Prediccion Poisson 
    st.subheader("Prediccion poisson")
    prediccion = predecir_poisson(df_ultimos1, df_ultimos2, equipo1, equipo2)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Victoria " + equipo1, f"{prediccion['Prob Victoria ' + equipo1]}%")
    col2.metric("Empate", f"{prediccion['Prob Empate']}%")
    col3.metric("Victoria " + equipo2, f"{prediccion['Prob Victoria ' + equipo2]}%")
    
    # Mostrar gráfico de predicción
    fig_poisson = graficar_prediccion_poisson(prediccion, equipo1, equipo2)
    st.plotly_chart(fig_poisson, use_container_width=True)

with tab2:
    #grafica de goles anotados
    st.header("Forma reciente")
    st.subheader("Goles anotados")
    fig_anotados = graficar_rendimiento_reciente(df_ultimos1, df_ultimos2, equipo1, equipo2)
    st.plotly_chart(fig_anotados, use_container_width=True)
    
    #grafica de goles recibidos
    st.subheader("Comparativa de goles recibidos")
    fig_recibidos = graficar_goles_recibidos(df_ultimos1, df_ultimos2, equipo1, equipo2)
    st.plotly_chart(fig_recibidos, use_container_width=True)

with tab3:
#grafica de radar
    st.subheader("Radar comparativo")
    fig_radar = graficar_radar(df_ultimos1, df_ultimos2, equipo1, equipo2)
    st.plotly_chart(fig_radar, use_container_width=True)