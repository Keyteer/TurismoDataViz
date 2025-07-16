import plotly.graph_objects as go
import pandas as pd

'''import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))'''
from utils.textos_idioma import textos


INDICADORES_DISPONIBLES = {
    "arrivals": "International tourism, number of arrivals",
    "departures": "International tourism, number of departures",
    "receipts_total": "International tourism, receipts (current US$)",
    "receipts_travel": "International tourism, receipts for travel items (current US$)",
    "receipts_transport": "International tourism, receipts for passenger transport items (current US$)",
    "expenditures_total": "International tourism, expenditures (current US$)",
    "expenditures_travel": "International tourism, expenditures for travel items (current US$)",
    "expenditures_transport": "International tourism, expenditures for passenger transport items (current US$)",
}

def opciones_dropdown_indicadores(idioma="es"):
    t = textos.get(idioma)
    return [
        {"label": t["indicadores_df1"][key], "value": key}
        for key in INDICADORES_DISPONIBLES
    ]

def generar_plot4(df, id_indicador, rango_anios, idioma="es"):
    t = textos.get(idioma)
    indicador = INDICADORES_DISPONIBLES[id_indicador]

## CREACIÓN DEL DATAFRAME:
    # Filtrar por indicador e intervalo de años
    df_filtrado = df[(df["Series Name"] == indicador) &
        (df["Year"] >= rango_anios[0]) & (df["Year"] <= rango_anios[1])]
    # Agrupar por país y calcular suma total
    df_agrupado = df_filtrado.groupby(
        ["Country Name", "Nombre Español"], as_index=False
    )["Value"].sum()
    # Ordenar de mayor a menor
    df_ordenado = df_agrupado.sort_values("Value", ascending=False)
    # Elegir columna de nombre según idioma
    nombre_col = "Country Name" if idioma == "en" else "Nombre Español"
    # Agregar numero tipo rank
    df_ordenado["Rank"] = range(1, len(df_ordenado) + 1)
    df_ordenado["Label"] = df_ordenado["Rank"].astype(str)

## CREACIÓN DEL GRÁFICO:
    # Seleccionar umbral
    umbral = df_ordenado["Value"].max() * 0.3
    # Generar una lista de colores según umbral
    colores_texto = [
        "white" if v > umbral else "black"
        for v in df_ordenado["Value"]
    ]
    # Determinar posición del texto según umbral
    text_positions = [
        "inside" if v > umbral else "outside"
        for v in df_ordenado["Value"]
    ]
    # Asignar valores al plot
    fig = go.Figure(go.Bar(
        x=df_ordenado["Value"],
        y=df_ordenado["Label"], # Usar Rank como etiqueta
        orientation="h",
        marker=dict(
            color='#1f77b4',  # Color azul
            line=dict(color='black', width=0.7)  # Borde negro
        ),
        text=df_ordenado[nombre_col], # Texto a mostrar
        textposition=text_positions, # Posición del texto
        textfont=dict(size=12), # Tamaño de texto
        textfont_color=colores_texto # Color del texto
    ))
    # Añadir etiquetas y configuracion del plot
    fig.update_layout(
        xaxis_title=t["eje_x_valor_plot4"],
        template="plotly_white",
        width=200,
        height=6000,
        margin=dict(l=10, r=10, t=10, b=10), # Ajustar márgenes
        yaxis=dict(autorange="reversed"),  # País con más valor arriba
    )

    return fig

if __name__ == "__main__":
    from utils.cargarDataframes import df1
    df = df1(path = "../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")
    indicador = "receipts_total"
    rango_anios = (2000, 2020)
    fig = generar_plot4(df, indicador, rango_anios, idioma="es")
    fig.show()