import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import math
import streamlit as st

#funcion resumen h2h
def resumen_head_to_head(df_h2h, equipo1, equipo2):
    #Determinar ganador de cada partido
    def determinar_ganador(row):
        if row["Goles Local"] > row["Goles Visitante"]:
            return row["Local"]
        elif row["Goles Visitante"] > row["Goles Local"]:
            return row["Visitante"]
        else:
            return "Empate"
        
    df_h2h["Ganador"] = df_h2h.apply(determinar_ganador, axis=1)
    
    total = len(df_h2h)
    victorias1 = sum(df_h2h["Ganador"] == equipo1)
    victorias2 = sum(df_h2h["Ganador"] == equipo2)
    empates = sum(df_h2h["Ganador"] == "Empate")

    goles1 = df_h2h["Goles Local"][df_h2h["Local"] == equipo1].sum() + df_h2h["Goles Visitante"][df_h2h["Visitante"] == equipo1].sum()
    goles2 = df_h2h["Goles Local"][df_h2h["Local"] == equipo2].sum() + df_h2h["Goles Visitante"][df_h2h["Visitante"] == equipo2].sum()

    return {
        "Partidos Jugados": total,
        f"Victorias {equipo1}": victorias1,
        f"Victorias {equipo2}": victorias2,
        "Empates": empates,
        f"Goles {equipo1}": goles1,
        f"Goles {equipo2}": goles2
    }
    
#funcion obtener partidos donde los equipos han jugado
def obtener_partidos_equipo(nombre_equipo, ruta="data/partidos.xlsx", hoja="Enfrentamientos", max_partidos=5):
    try:
        df = pd.read_excel(ruta, sheet_name=hoja)
        if not pd.api.types.is_datetime64_any_dtype(df["Fecha"]):
            df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce", dayfirst=True)
        
        #filtrar partidos donde el equipo ha jugado
        partidos_equipo = df[(df["Local"] == nombre_equipo) | (df["Visitante"] == nombre_equipo)]
        
        #ordenar de forma descendente por fecha
        partidos_equipo = partidos_equipo.sort_values(by="Fecha", ascending=False)
        
        #retornar los últimos 
        return partidos_equipo.head(max_partidos).reset_index(drop=True)
    
    except Exception as e:
        return pd.DataFrame({"Error": [f"No se pudieron cargar los partidos: (e)"]})

#Funcion de probabilidades de poisson
def poisson_prob(lmbda, k):
    """Probabilidad de k goles con media lmbda"""
    return (lmbda**k * math.exp(-lmbda)) / math.factorial(k)

def predecir_poisson(df1, df2, equipo1, equipo2, max_goles=5):
    """
    Calcula probabilidades de victoria/empate/derrota usando modelo Poisson
    """
    # Promedio de goles a favor
    goles1 = df1.apply(lambda r: r["Goles Local"] if r["Local"] == equipo1 else r["Goles Visitante"], axis=1).mean()
    goles2 = df2.apply(lambda r: r["Goles Local"] if r["Local"] == equipo2 else r["Goles Visitante"], axis=1).mean()

    # Promedio de goles en contra
    encajados1 = df1.apply(lambda r: r["Goles Visitante"] if r["Local"] == equipo1 else r["Goles Local"], axis=1).mean()
    encajados2 = df2.apply(lambda r: r["Goles Visitante"] if r["Local"] == equipo2 else r["Goles Local"], axis=1).mean()

    # Potencial ofensivo y defensivo
    lambda_equipo1 = (goles1 + encajados2) / 2
    lambda_equipo2 = (goles2 + encajados1) / 2

    # Calcular probabilidades de todos los marcadores posibles
    prob_equipo1 = 0
    prob_equipo2 = 0
    prob_empate = 0

    for goles_a in range(max_goles + 1):
        for goles_b in range(max_goles + 1):
            p = poisson_prob(lambda_equipo1, goles_a) * poisson_prob(lambda_equipo2, goles_b)
            if goles_a > goles_b:
                prob_equipo1 += p
            elif goles_a < goles_b:
                prob_equipo2 += p
            else:
                prob_empate += p

    return {
        "Prob Victoria " + equipo1: round(prob_equipo1 * 100, 2),
        "Prob Empate": round(prob_empate * 100, 2),
        "Prob Victoria " + equipo2: round(prob_equipo2 * 100, 2)
    }