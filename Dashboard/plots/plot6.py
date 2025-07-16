from dash import dash_table
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.textos_idioma import textos


INDICADORES_DISPONIBLES = {
    "receipts_exports": "International tourism, receipts (% of total exports)",
    "expenditures_imports": "International tourism, expenditures (% of total imports)"
}

def plot6_indicadores(idioma="es"):
    t = textos.get(idioma)
    return [
        {"label": t["indicadores_df1"][key], "value": key}
        for key in INDICADORES_DISPONIBLES
    ]

def generar_plot6(df, id_indicador, rango_anios, idioma="es"):
    indicador = INDICADORES_DISPONIBLES[id_indicador]

    ## CREACIÓN DEL DATAFRAME:
    df_filtrado = df[(df["Series Name"] == indicador) &
                     (df["Year"] >= rango_anios[0]) & (df["Year"] <= rango_anios[1])]
    # Agrupar por país y calcular promedio
    df_agrupado = df_filtrado.groupby(
        ["Country Name", "Nombre Español"], as_index=False
    )["Value"].mean()
    # Ordenar de mayor a menor
    df_ordenado = df_agrupado.sort_values("Value", ascending=False)
    # Elegir columna de nombre según idioma
    nombre_col = "Country Name" if idioma == "en" else "Nombre Español"
    # Agregar número tipo rank
    df_ordenado["Rank"] = range(1, len(df_ordenado) + 1)
    # Formatear valor con % y sin decimales
    df_ordenado["Value_formateado"] = df_ordenado["Value"].round(0).astype(int).astype(str) + "%"
    # Preparar dataframe para la tabla con columnas separadas
    df_tabla = df_ordenado[["Rank", nombre_col, "Value_formateado"]]

    ## CREACIÓN DE LA TABLA:
    tabla = dash_table.DataTable(
        columns=[{"name": "", "id": col} for col in df_tabla.columns],
        data=df_tabla.to_dict("records"),
        sort_action="native",
        filter_action="none",
        page_action="none",
        style_table={
            "overflowY": "auto",
            "maxHeight": "300px",
            "width": "200px"
        },
        style_cell={
            "padding": "6px",
            "fontFamily": "Arial",
            "fontSize": "10px",
            "border": "1px solid #ddd",
            "whiteSpace": "nowrap",
            "textOverflow": "ellipsis",
            "overflow": "hidden",
            "maxWidth": "1px"
        },
        style_cell_conditional=[
            {"if": {"column_id": "Rank"},
                "textAlign": "center",
                "width": "16%"},
            {"if": {"column_id": nombre_col},
                "textAlign": "left",
                "borderRight": "right",
                "width": "auto"},
            {"if": {"column_id": "Value_formateado"},
                "textAlign": "center",
                "width": "18%"}
        ],
        style_header={
            "display": "none"
        }
    )
    return tabla





if __name__ == "__main__":
    from dash import Dash, html
    from utils.cargarDataframes import df1

    df = df1(path="../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")
    indicador = "receipts_exports"
    rango_anios = (2015, 2020)
    tabla = generar_plot4(df, indicador, rango_anios, idioma="es")

    app = Dash(__name__)
    app.layout = html.Div([
        tabla
    ])

    app.run(debug=True)