import plotly.graph_objects as go
import pandas as pd

'''import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))'''


# Evolución de ingresos por turismo vs PIB (Gráfico área apilada / no apilada)
def generar_plot1(df, pais, apilar=True):

## CREACIÓN DEL DATAFRAME:
    # Filtrar datos de ingresos por turismo
    df_turismo = df[
        (df["Series Name"] == "International tourism, receipts (current US$)") &
        (df["Nombre Español"] == pais)
    ][["Year", "Value"]].rename(columns={"Value": "Turismo"})
    # Filtrar datos de PIB
    df_pib = df[
        (df["Series Name"] == "GDP (current US$)") &
        (df["Nombre Español"] == pais)
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
        name="Turismo",
        fill=fill_turismo,
        line=dict(width=0.5),
        stackgroup="one" if apilar else None,
    ))
    # Añadir trazas para PIB restante
    fig.add_trace(go.Scatter(
        x=df_merge["Year"],
        y=df_merge["PIB restante"],
        mode="lines",
        name="PIB restante",
        fill=fill_pib,
        line=dict(width=0.5),
        stackgroup="one" if apilar else None,
    ))
    # Elegir título según si es apilado o no
    if apilar is True:
        titulo = f"Aporte del turismo al PIB de {pais} (apilado)"
    else:
        titulo = f"Aporte del turismo al PIB de {pais} (no apilado)"
    # Configurar el diseño del gráfico
    fig.update_layout(
        title=titulo,
        xaxis_title="Año",
        yaxis_title="PIB (US)",
        template="plotly_white",
        legend_title="Fuente"
    )
    return fig

# Para probarlo directamente:
if __name__ == "__main__":
    from utils.cargarDataframes import df1
    df = df1(path = "../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")
    # Apilado
    fig1 = generar_plot1(df, "Maldivas", apilar=True)
    fig1.show()

    # No apilado
    fig2 = generar_plot1(df, "Maldivas", apilar=False)
    fig2.show()