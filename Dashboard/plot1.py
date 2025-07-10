import plotly.graph_objects as go
import pandas as pd

from utils.cargarDataframes import df1
from utils.traducirPais import traducir_pais


# Evolución de ingresos por turismo vs PIB (Gráfico área apilada / no apilada)
def generar_plot1(df, pais, apilar=True):

## CREACIÓN DEL DATAFRAME:
    # Filtrar datos de ingresos por turismo
    df_turismo = df[
        (df["Series Name"] == "International tourism, receipts (current US$)") &
        (df["Country Name"] == pais)
    ][["Year", "Value"]].rename(columns={"Value": "Turismo"})
    # Filtrar datos de PIB
    df_pib = df[
        (df["Series Name"] == "GDP (current US$)") &
        (df["Country Name"] == pais)
    ][["Year", "Value"]].rename(columns={"Value": "PIB"})
    # Combinar por año
    df_merge = pd.merge(df_pib, df_turismo, on="Year", how="inner")
    # Calcular PIB restante
    df_merge["PIB restante"] = df_merge["PIB"] - df_merge["Turismo"]

## CREACIÓN DEL GRÁFICO:
    fill_turismo = "tonexty" if apilar else "tozeroy"
    fill_pib = "tonexty" if apilar else "tozeroy"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_merge["Year"],
        y=df_merge["Turismo"],
        mode="lines",
        name="Turismo",
        fill=fill_turismo,
        line=dict(width=0.5),
        stackgroup="one" if apilar else None,
    ))

    fig.add_trace(go.Scatter(
        x=df_merge["Year"],
        y=df_merge["PIB restante"],
        mode="lines",
        name="PIB restante",
        fill=fill_pib,
        line=dict(width=0.5),
        stackgroup="one" if apilar else None,
    ))

    if apilar is True:
        titulo = f"Aporte del turismo al PIB de {traducir_pais(pais)} (apilado)"
    else:
        titulo = f"Aporte del turismo al PIB de {traducir_pais(pais)} (no apilado)"

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
    df = df1()
    # Apilado
    fig1 = generar_plot1(df, "Maldives", apilar=True)
    fig1.show()

    # No apilado
    fig2 = generar_plot1(df, "Maldives", apilar=False)
    fig2.show()