import plotly.express as px
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.textos_idioma import textos

INDICADORES_DISPONIBLES = {
    "arrivals": "International tourism, number of arrivals",
    "departures": "International tourism, number of departures"
}

def plot4_indicadores(idioma="es"):
    t = textos.get(idioma)
    return [
        {"label": t["indicadores_df1"][key], "value": key}
        for key in INDICADORES_DISPONIBLES
    ]

def generar_plot7(df, Country_Code, id_indicador, idioma="es"):
    
    t = textos.get(idioma)
    indicador = INDICADORES_DISPONIBLES[id_indicador]

## CREACIÓN DEL DATAFRAME:

    df_arrivals = df[
        (df["Series Name"] == indicador) &
        (df["Country Code"] == Country_Code)
    ][["Year", "Value"]]

## CREACIÓN DEL GRÁFICO:

    fig = px.line(
        df_arrivals,
        x="Year",
        y="Value",
        labels={
            "Year": t["label_anio_plot7"],
            "Value": t["indicadores_df1"][id_indicador],
        },
        markers=True,
        template="plotly_white",
        color_discrete_sequence=["#0dcf75"]
    )

    

    return fig

if __name__ == "__main__":
    from utils.cargarDataframes import df1
    df = df1(path = "../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")
    
    fig1 = generar_plot7(df, "USA", "arrivals", idioma="es")
    fig1.show()