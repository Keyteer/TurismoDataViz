import plotly.graph_objects as go
import matplotlib.colors as mcolors
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
    "receipts_exports": "International tourism, receipts (% of total exports)",
    "expenditures_imports": "International tourism, expenditures (% of total imports)",
    "GDP": "GDP (current US$)"
}

def plot5_indicadores(idioma="es"):
    t = textos.get(idioma)
    return [
        {"label": t["indicadores_df1"][key], "value": key}
        for key in INDICADORES_DISPONIBLES
    ]

def generar_plot5(df, id_indicador_x, id_indicador_y, rango_anios, idioma="es", filter_top=0):
    t = textos.get(idioma)
    indicador_x = INDICADORES_DISPONIBLES[id_indicador_x]
    indicador_y = INDICADORES_DISPONIBLES[id_indicador_y]

## CREACIÓN DEL DATAFRAME:
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
    # Aplicar filtro top solo si válido
    if filter_top > 0 and filter_top < len(df_merge):
        df_merge = df_merge.iloc[filter_top:]
    # Verificar que haya datos
    if df_merge.empty:
        raise ValueError("No hay datos suficientes para mostrar el gráfico.")

## CREACIÓN DEL PLOT:
    # Creación gradientes de color
    color_inicio = "#0d8b4e"
    color_final = "#a6e3c2"
    valores_norm = (df_merge["X"] - df_merge["X"].min()) / (df_merge["X"].max() - df_merge["X"].min())
    valores_norm = valores_norm.fillna(0)
    cmap = mcolors.LinearSegmentedColormap.from_list("verde_gradiente", [color_inicio, color_final])
    colores_puntos = [mcolors.to_hex(cmap(v)) for v in valores_norm]
    # Crear el gráfico de dispersión
    fig = go.Figure()
    for idx, (_, row) in enumerate(df_merge.iterrows()):
        fig.add_trace(go.Scatter(
            x=[row["X"]],
            y=[row["Y"]],
            mode="markers",
            marker=dict(
                color=colores_puntos[idx],  # usar idx en lugar de i
                size=10,
                line=dict(width=0.5, color="black")
            ),
            hovertemplate=(
                f"{row[nombre_col]}<br>"
                f"{t['indicadores_df1'][id_indicador_x]}: {row['X']:,}<br>"
                f"{t['indicadores_df1'][id_indicador_y]}: {row['Y']:,}<extra></extra>"
            ),
            showlegend=False
        ))

    fig.update_layout(
        xaxis_title=t["indicadores_df1"][id_indicador_x],
        yaxis_title=t["indicadores_df1"][id_indicador_y],
        template="plotly_white",
        margin=dict(l=40, r=10, t=40, b=40)
    )

    return fig

if __name__ == "__main__":
    from utils.cargarDataframes import df1
    df = df1(path = "../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")
    fig = generar_plot5(df, "expenditures_total", "receipts_total", (2015, 2020), idioma="en", filter_top=3)
    fig.show()