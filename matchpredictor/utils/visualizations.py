import pandas as pd
import plotly.graph_objects as go

#funcion para obtener la grafica de goles anotados en sus ultimos 5 partidos
def graficar_rendimiento_reciente(df1, df2, nombre1, nombre2):
    
    df1["Fecha"] = pd.to_datetime(df1["Fecha"], errors='coerce')
    df2["Fecha"] = pd.to_datetime(df2["Fecha"], errors='coerce')
    
    df1 = df1.sort_values(by="Fecha")
    df2 = df2.sort_values(by="Fecha")
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df1["Fecha"],
        y=df1.apply(lambda row: row["Goles Local"] if row["Local"] == nombre1 else row["Goles Visitante"], axis=1),
        name=nombre1,
        marker_color='blue'
    ))

    fig.add_trace(go.Bar(
        x=df2["Fecha"],
        y=df2.apply(lambda row: row["Goles Local"] if row["Local"] == nombre2 else row["Goles Visitante"], axis=1),
        name=nombre2,
        marker_color='red'
    ))

    fig.update_layout(
        title="Goles anotados en los últimos partidos",
        xaxis_title="Fecha",
        yaxis_title="Goles",
        barmode='group'
    )

    return fig

#funcion para la grafica de goles recibidos
def graficar_goles_recibidos (df1, df2, nombre1, nombre2):
    
    df1["Fecha"] = pd.to_datetime(df1["Fecha"], errors='coerce')
    df2["Fecha"] = pd.to_datetime(df2["Fecha"], errors='coerce')
    
    #ordenar cronológicamente
    df1 = df1.sort_values(by="Fecha")
    df2 = df2.sort_values(by="Fecha")
    
    fig = go.Figure()

    #goles recibidos por equipo1
    fig.add_trace(go.Bar(
        x=df1["Fecha"],
        y=df1.apply(lambda row: row["Goles Visitante"] if row["Local"] == nombre1 else row["Goles Local"], axis=1),
        name=f"Goles recibidos {nombre1}",
        marker_color='lightblue'
    ))
    
    #goles recibidos por equipo2
    fig.add_trace(go.Bar(
        x=df2["Fecha"],
        y=df2.apply(lambda row: row["Goles Visitante"] if row["Local"] == nombre2 else row["Goles Local"], axis=1),
        name=f"Goles recibidos {nombre2}",
        marker_color='lightcoral'
    ))

    fig.update_layout(
        title="Goles recibidos en los últimos partidos",
        xaxis=dict(
            title = "Fecha",
            tickformat = "%d-%m"
        ),
        yaxis_title="Goles Recibidos",
        barmode='group',
    )

    return fig

#funcion del grafico radar goles anotados, goles recibidos, % victorias, empates y derrotas
def graficar_radar(df1, df2, nombre1, nombre2):
    #calcular metricas:
    def calcular_stats(df, nombre):
        goles_anotados = df.apply(lambda row: row["Goles Local"] if row["Local"] == nombre else row["Goles Visitante"], axis=1).mean()
        goles_recibidos = df.apply(lambda row: row["Goles Visitante"] if row["Local"] == nombre else row["Goles Local"], axis=1).mean()
        
        #determinar resultados
        victorias = sum((df["Local"] == nombre) & (df["Goles Local"] > df["Goles Visitante"])) + \
                    sum((df["Visitante"] == nombre) & (df["Goles Visitante"] > df["Goles Local"]))
        empates = sum(df["Goles Local"] == df["Goles Visitante"])
        derrotas = len(df) - victorias - empates
        
        return [goles_anotados, goles_recibidos, victorias, empates, derrotas]
    
    stats1 = calcular_stats(df1, nombre1)
    stats2 = calcular_stats(df2, nombre2)
    
    #ejes del radar
    categorias = ["Goles Anotados", "Goles Recibidos", "Victorias", "Empates", "Derrotas"]
    
    #crear el radar
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=stats1,
        theta=categorias,
        fill='toself',
        name=nombre1,
        line_color='blue'
    ))

    fig.add_trace(go.Scatterpolar(
        r=stats2,
        theta=categorias,
        fill='toself',
        name=nombre2,
        line_color='red'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(max(stats1), max(stats2)) + 1])
        ),
        showlegend=True,
        title="Comparativa de estadísticas globales (Radar Chart)"
    )

    return fig

#Genera un grafico con probabilidades de poisson
def graficar_prediccion_poisson(prediccion, equipo1, equipo2):
    """
    Genera un gráfico de barras con probabilidades de Poisson
    """
    etiquetas = [f"Victoria {equipo1}", "Empate", f"Victoria {equipo2}"]
    valores = [
        prediccion[f"Prob Victoria {equipo1}"],
        prediccion["Prob Empate"],
        prediccion[f"Prob Victoria {equipo2}"]
    ]

    fig = go.Figure(go.Bar(
        x=etiquetas,
        y=valores,
        marker_color=['blue', 'gray', 'red'],
        text=[f"{v}%" for v in valores],
        textposition='auto'
    ))

    fig.update_layout(
        title="Probabilidades de resultado (Modelo Poisson)",
        xaxis_title="Resultado posible",
        yaxis_title="Probabilidad (%)",
        yaxis=dict(range=[0, 100])
    )

    return fig