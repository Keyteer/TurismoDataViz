import plotly.graph_objects as go
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.textos_idioma import textos

def generar_plot4(df, indicador, rango_anios, idioma="es"):
    t = textos.get(idioma)

## CREACIÓN DEL DATAFRAME:
    # Filtrar por indicador e intervalo de años
    df_filtrado = df[(df["Series Name"] == indicador) &
        (df["Year"] >= rango_anios[0]) & (df["Year"] <= rango_anios[1])]
    # Agrupar por país y calcular promedio
    df_agrupado = df_filtrado.groupby(
        ["Country Name", "Nombre Español"], as_index=False
    )["Value"].sum()
    # Ordenar de mayor a menor
    df_ordenado = df_agrupado.sort_values("Value", ascending=False)
    # Elegir columna de nombre según idioma
    nombre_col = "Country Name" if idioma == "en" else "Nombre Español"

## CREACIÓN DEL GRÁFICO:
    fig = go.Figure(go.Bar(
        x=df_ordenado["Value"],
        orientation="h",
        marker=dict(color='teal'),
        text = df_ordenado[nombre_col],
        textposition = "inside",
        insidetextanchor = "middle",
        textfont = dict(color="white", size=20)
    ))
    fig.update_layout(
        xaxis_title=t["eje_x_valor_plot4"],
        yaxis_title=t["eje_y_pais_plot4"],
        template="plotly_white",
        width=300,
        height=8000,
        margin=dict(l=20, r=20, t=20, b=20), # Ajustar márgenes
        yaxis=dict(autorange="reversed")  # País con más valor arriba
    )

    return fig

if __name__ == "__main__":
    from utils.cargarDataframes import df1
    df = df1(path = "../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")
    #indicador = "International tourism, number of arrivals"
    #indicador = "International tourism, number of departures"
    indicador ="International tourism, receipts (current US$)"
    #indicador ="International tourism, receipts for travel items (current US$)"
    #indicador ="International tourism, receipts for passenger transport items (current US$)"
    #indicador ="International tourism, expenditures (current US$)"
    #indicador ="International tourism, expenditures for travel items (current US$)"
    #indicador ="International tourism, expenditures for passenger transport items (current US$)"

    rango_anios = (2000, 2020)
    fig = generar_plot4(df, indicador, rango_anios, idioma="es")
    fig.show()

