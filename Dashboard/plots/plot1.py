import plotly.graph_objects as go
import pandas as pd

'''import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))'''
from utils.textos_idioma import textos


# Evolución de ingresos por turismo vs PIB (Gráfico área apilada / no apilada)
def generar_plot1(df, Country_Code, apilar=True, idioma="es"):
    t = textos.get(idioma)

## CREACIÓN DEL DATAFRAME:
    # Filtrar datos de ingresos por turismo
    df_turismo = df[
        (df["Series Name"] == "International tourism, receipts (current US$)") &
        (df["Country Code"] == Country_Code)
    ][["Year", "Value"]].rename(columns={"Value": "Turismo"})
    # Filtrar datos de PIB
    df_pib = df[
        (df["Series Name"] == "GDP (current US$)") &
        (df["Country Code"] == Country_Code)
    ][["Year", "Value"]].rename(columns={"Value": "PIB"})
    # Combinar por año
    df_merge = pd.merge(df_pib, df_turismo, on="Year", how="inner")
    # Calcular PIB restante
    df_merge["PIB restante"] = df_merge["PIB"] - df_merge["Turismo"]

## CREACIÓN DEL GRÁFICO:
    # Configuración del relleno según si es apilado o no
    fill_turismo = "tonexty" if apilar else "tozeroy"
    fill_pib = "tonexty" if apilar else "tozeroy"
    # Crear la figura
    fig = go.Figure()
    # Añadir trazas para Turismo
    fig.add_trace(go.Scatter(
        x=df_merge["Year"],
        y=df_merge["Turismo"],
        mode="lines",
        name=t["turismo"],
        fill=fill_turismo,
        line=dict(width=0.5, color="black"),
        fillcolor='rgba(153, 218, 255, 0.4)',
        stackgroup="one" if apilar else None,
    ))
    # Añadir trazas para PIB restante
    fig.add_trace(go.Scatter(
        x=df_merge["Year"],
        y=df_merge["PIB restante"],
        mode="lines",
        name=t["pib_restante"],
        fill=fill_pib,
        line=dict(width=0.5, color="black"),
        fillcolor='rgba(126, 217, 87, 0.4)',
        stackgroup="one" if apilar else None,
    ))
    # Elegir nombre del país según el idioma
    if idioma == "es":
        nombre_pais =df[df["Country Code"] == Country_Code]["Nombre Español"].iloc[0]
    else:
        nombre_pais = df[df["Country Code"] == Country_Code]["Country Name"].iloc[0]
    # Elegir título según si es apilado o no
    if apilar:
       titulo = t["grafico_titulo_apilado"].format(pais=nombre_pais)
    else:
       titulo = t["grafico_titulo_no_apilado"].format(pais=nombre_pais)
    # Configurar el diseño del gráfico
    fig.update_layout(
        xaxis_title=t["eje_x"],
        yaxis_title=t["eje_y"],
        template="plotly_white",
        legend_title=t["leyenda"],
        height=395,
        # leyenda custom segun t["turismo"] y t["pib_restante"]


    )
    return titulo, fig

# Para probarlo directamente:
if __name__ == "__main__":
    from utils.cargarDataframes import df1
    df = df1(path = "../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")
    # Apilado
    fig1 = generar_plot1(df, "MDV", apilar=True, idioma="es")
    fig1.show()

    # No apilado
    fig2 = generar_plot1(df, "MDV", apilar=False, idioma="en")
    fig2.show()