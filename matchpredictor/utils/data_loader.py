import streamlit as st
import pandas as pd

#Funcion para optimizar
@st.cache_data
def cargar_datos(ruta="data/partidos.xlsx"):
    """
    Carga y cachea los datos de equipos y enfrentamientos desde el Excel.
    """
    try:
        # Cargar hoja de equipos
        df_equipos = pd.read_excel(ruta, sheet_name="Equipos")

        # Cargar hoja de enfrentamientos
        df_enfrentamientos = pd.read_excel(ruta, sheet_name="Enfrentamientos")
        df_enfrentamientos["Fecha"] = pd.to_datetime(df_enfrentamientos["Fecha"], errors="coerce", dayfirst=True)

        return df_equipos, df_enfrentamientos

    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame(), pd.DataFrame()