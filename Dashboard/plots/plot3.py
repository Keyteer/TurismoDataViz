import plotly.express as px
import pandas as pd

'''import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))'''
from utils.textos_idioma import textos

COLORES_INDICADORES = {
    "arrivals": "#0d66c6",
    "departures": "#06ae3b",
    "receipts_total": "#1082c4",
    "receipts_travel": "#0f61c5",
    "receipts_transport": "#1264C7",
    "expenditures_total": "#09b252",
    "expenditures_travel": "#45C019", 
    "expenditures_transport": "#1ac542" 
}

OPCIONES_DISPONIBLES = {
    "arrivals": "International tourism, number of arrivals",
    "receipts_total": "International tourism, receipts  (current US$)",
    "receipts_travel": "International tourism, receipts for travel items (current US$)",
    "receipts_transport": "International tourism, receipts for passenger transport items (current US$)",
    }

INDICADORES_DISPONIBLES = {
    "arrivals": "International tourism, number of arrivals",
    "receipts_total": "International tourism, receipts (current US$)",
    "receipts_travel": "International tourism, receipts for travel items (current US$)",
    "receipts_transport": "International tourism, receipts for passenger transport items (current US$)",
    "departures": "International tourism, number of departures",
    "expenditures_total": "International tourism, expenditures (current US$)",
    "expenditures_travel": "International tourism, expenditures for travel items (current US$)",
    "expenditures_transport": "International tourism, expenditures for passenger transport items (current US$)",
}

def plot3_indicadores(idioma="es"):
    t = textos.get(idioma)
    return [
        {"label": t["indicadores_df1"][key], "value": key}
        for key in OPCIONES_DISPONIBLES
    ]

def generar_plot3(df, Country_Code,id_indicador_1, id_indicador_2, rango_anio, idioma="es"):
    
    t = textos.get(idioma)
    indicador_1 = INDICADORES_DISPONIBLES[id_indicador_1]
    indicador_2 = INDICADORES_DISPONIBLES[id_indicador_2]

## CREACIÓN DEL DATAFRAME:

    # Filtrar el DataFrame para obtener los datos de los indicadores seleccionados y el país
    df_1 = df[
        (df["Series Name"] == indicador_1) &
        (df["Country Code"] == Country_Code) &
        (df["Year"] >= rango_anio[0]) & (df["Year"] <= rango_anio[1])
    ][["Year", "Value"]].rename(columns={"Value": "Value1"})
    df_2 = df[
        (df["Series Name"] == indicador_2) &
        (df["Country Code"] == Country_Code) &
        (df["Year"] >= rango_anio[0]) & (df["Year"] <= rango_anio[1])
    ][["Year", "Value"]].rename(columns={"Value": "Value2"})

    # Unir los DataFrames filtrados por el año
    df_d = pd.merge(df_1, df_2, on="Year", how="inner")
    
    # Crear DataFrame para el pie chart con los valores normalizados
    pie_data = pd.DataFrame({
        'Categoria': [t["indicadores_df1"][id_indicador_1], t["indicadores_df1"][id_indicador_2]],
        'Valores': [df_d['Value1'].sum(), df_d['Value2'].sum()]
    })
    
## CREACIÓN DEL GRÁFICO:
    
    # Asignar colores fijos según el orden de los indicadores
    if pie_data['Valores'].iloc[0] > pie_data['Valores'].iloc[1]:
        colores_fijos = [
            COLORES_INDICADORES[id_indicador_1],
            COLORES_INDICADORES[id_indicador_2]
        ]
    else:
        colores_fijos = [
            COLORES_INDICADORES[id_indicador_2],
            COLORES_INDICADORES[id_indicador_1]
        ]

    # Crear el gráfico de pastel
    fig = px.pie(
        pie_data,
        values='Valores',
        names='Categoria',
        color_discrete_sequence=colores_fijos,
        hover_data=['Valores']
    )

    fig.update_traces(
        legendgroup=None,
        showlegend=True
    )

    fig.update_layout(
        legend=dict(
            itemclick=False,  
            itemdoubleclick=False,
            orientation="h",           
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=11),

        ),
        margin=dict(l=20, r=20, t=5, b=10),  # left, right, top, bottom
        autosize=True,
        height=255,
    )

    return fig

if __name__ == "__main__":
    from utils.cargarDataframes import df1
    df = df1(path = "../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")

     # Ejemplo sin filtro de año
    fig1 = generar_plot3(df, "USA","arrivals","departures", {2021,2021}, idioma="es")
    if fig1:
        fig1.show()
    
    # Ejemplo con filtro de año específico
    fig2 = generar_plot3(df, "USA","arrivals","departures", {2015,2021}, idioma="es")
    if fig2:
        fig2.show()