import streamlit as st
import pandas as pd

#Funcion para optimizar
@st.cache_data
def cargar_datos():
    ruta = os.path.join(os.path.dirname(__file__), "..", "data", "partidos.xlsx")
    ruta = os.path.abspath(ruta)

    df_equipos = pd.read_excel(ruta, sheet_name="Equipos")
    df_enfrentamientos = pd.read_excel(ruta, sheet_name="Enfrentamientos")
    df_enfrentamientos["Fecha"] = pd.to_datetime(df_enfrentamientos["Fecha"], errors="coerce", dayfirst=True)

    return df_equipos, df_enfrentamientos
