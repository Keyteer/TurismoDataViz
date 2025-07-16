import plotly.express as px
import pandas as pd


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

def generar_plot5(df, id_indicador_x, id_indicador_y, rango_anios, idioma="es", filter_top=0):
    t = textos.get(idioma)
    indicador_x = INDICADORES_DISPONIBLES[id_indicador_x]
    indicador_y = INDICADORES_DISPONIBLES[id_indicador_y]

    # Filtrar por indicadores y rango de años
    df_x = df[(df["Series Name"] == indicador_x) &
              (df["Year"] >= rango_anios[0]) & (df["Year"] <= rango_anios[1])]
    df_y = df[(df["Series Name"] == indicador_y) &
              (df["Year"] >= rango_anios[0]) & (df["Year"] <= rango_anios[1])]

    # Agrupar por país y sumar valores
    df_x_agg = df_x.groupby(["Country Name", "Nombre Español"], as_index=False)["Value"].sum().rename(columns={"Value": "X"})
    df_y_agg = df_y.groupby(["Country Name", "Nombre Español"], as_index=False)["Value"].sum().rename(columns={"Value": "Y"})

    # Unir ambos indicadores por país
    df_merge = pd.merge(df_x_agg, df_y_agg, on=["Country Name", "Nombre Español"], how="inner")

    # Eliminar top 3 países por X
    df_merge = df_merge.sort_values("X", ascending=False).iloc[filter_top:]

    # Elegir columna de nombre según idioma
    nombre_col = "Country Name" if idioma == "en" else "Nombre Español"

    # Crear scatterplot con plotly express, nombres solo en hover
    fig = px.scatter(
        df_merge,
        x="X",
        y="Y",
        hover_name=nombre_col,
        labels={
            "X": t["indicadores_df1"][id_indicador_x],
            "Y": t["indicadores_df1"][id_indicador_y]
        }
    )
    fig.update_layout(template="plotly_white", margin=dict(l=40, r=10, t=40, b=40))
    return fig

if __name__ == "__main__":
    from utils.cargarDataframes import df1
    df = df1(path = "../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")
    fig = generar_plot5(df, "expenditures_total", "receipts_total", (2015, 2020), idioma="es", filter_top=3)
    fig.show()
