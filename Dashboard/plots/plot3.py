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

def plot4_indicadores(idioma="es"):
    t = textos.get(idioma)
    return [
        {"label": t["indicadores_df1"][key], "value": key}
        for key in INDICADORES_DISPONIBLES
    ]

def generar_plot3(df, Country_Code,id_indicador_1, id_indicador_2, year=2013, idioma="es"):
    
    t = textos.get(idioma)
    indicador_1 = INDICADORES_DISPONIBLES[id_indicador_1]
    indicador_2 = INDICADORES_DISPONIBLES[id_indicador_2]

## CREACIÓN DEL DATAFRAME:

    df_1 = df[
        (df["Series Name"] == indicador_1) &
        (df["Country Code"] == Country_Code) &
        (df["Year"] == year)
    ][["Year", "Value"]].rename(columns={"Value": "Arrivals"})
    df_2 = df[
        (df["Series Name"] == indicador_2) &
        (df["Country Code"] == Country_Code) &
        (df["Year"] == year)
    ][["Year", "Value"]].rename(columns={"Value": "Expenditures"})

    df_d = pd.merge(df_1, df_2, on="Year", how="inner")

    # Verificar si hay datos para ese año
    if df_d.empty:
        print(f"No hay datos disponibles para el año {year} en el país {Country_Code}")
        return None
    
    # Crear DataFrame para el pie chart con los valores normalizados
    # Normalizar los valores para que sean comparables en el pie chart
    arrivals_norm = df_d['Arrivals'].iloc[0] / 1000000  # Convertir a millones
    expenditures_norm = df_d['Expenditures'].iloc[0] / 1000000000  # Convertir a miles de millones
    
    pie_data = pd.DataFrame({
        'Categoria': ['Arrivals (Millions)', 'Expenditures (Billions USD)'],
        'Valores': [arrivals_norm, expenditures_norm]
    })
    
## CREACIÓN DEL GRÁFICO:
    # Título dinámico
    title = f"Tourism Arrivals vs Expenditures for {Country_Code} in {year}"

    fig = px.pie(
        pie_data,
        values='Valores',
        names='Categoria',
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set3,
        hover_data=['Valores']
    )
    
  

    print(df_d.head)

    return fig

if __name__ == "__main__":
    from utils.cargarDataframes import df1
    df = df1(path = "../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")

     # Ejemplo sin filtro de año
    fig1 = generar_plot3(df, "USA","arrivals","departures", idioma="es")
    if fig1:
        fig1.show()
    
    # Ejemplo con filtro de año específico
    fig2 = generar_plot3(df, "USA","arrivals","departures", year=2019, idioma="es")
    if fig2:
        fig2.show()