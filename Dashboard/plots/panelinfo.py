from dash import html
import dash_bootstrap_components as dbc

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
    "receipts_exports": "International tourism, receipts (% of total exports)",
    "expenditures_imports": "International tourism, expenditures (% of total imports)",
    "GDP": "GDP (current US$)"
}
INDICADORES_PORCENTUALES = {
    "receipts_exports",
    "expenditures_imports"
}

def generar_panel_info(df, country_code, rango_anios, idioma="es"):
    t = textos.get(idioma, {})
    etiquetas = t.get("indicadores_df1", {})
## CREACIÓN DEL DATAFRAME:
    # Filtrar país
    df_pais = df[df["Country Code"] == country_code]
    if df_pais.empty:
        return html.Div([html.P("País no encontrado")])
    # Filtrar por año
    if rango_anios:
        df_pais = df_pais[df_pais["Year"].between(rango_anios[0], rango_anios[1])]
    # Nombre del país según idioma
    col_nombre = "Country Name" if idioma == "en" else "Nombre Español"
    nombre_pais = df_pais[col_nombre].iloc[0]

## CREACIÓN DEL PANEL:
    # Crear tarjetas de indicadores
    tarjetas = []
    for key, serie in INDICADORES_DISPONIBLES.items():
        label = etiquetas.get(key, key)

        valores = df_pais[df_pais["Series Name"] == serie]["Value"]
        if valores.empty:
            valor = 0
        elif key in INDICADORES_PORCENTUALES:
            valor = valores.mean()
        else:
            valor = valores.sum()

        tarjetas.append(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Small(label, style={
                            "fontSize": "12px",
                            "fontFamily": "Arial, sans-serif"
                        }),
                        html.P(f"{valor:,.3f}", style={
                            "fontWeight": "bold",
                            "fontSize": "12px",
                            "margin": "0",
                            "fontFamily": "Arial, sans-serif"
                        })
                    ]),
                    className="shadow-sm h-100",
                    style={"padding": "4px"}
                ),
                width=12
            )
        )

    return dbc.Container([
        html.H6(
            t.get("titulo_panel_info", "Indicadores de {pais}").format(pais=nombre_pais),
            className="text-center",
            style={"fontSize": "13px", "marginBottom": "6px", "fontFamily": "Arial, sans-serif"}
        ),
        html.Div(
            dbc.Row(tarjetas, className="gx-2 gy-2"),
            style={
                "maxHeight": "215px",
                "overflowY": "auto"
            }
        )
    ], style={"width": "260px", "height": "250px", "padding": "5px"})


if __name__ == "__main__":
    from dash import Dash
    from utils.cargarDataframes import df1
    df = df1(path="../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")
    pais = "CHL"
    anio_inicio = 2000
    anio_fin = 2001
    panel_info = generar_panel_info(df, pais, idioma="en", anio_inicio=anio_inicio, anio_fin=anio_fin)
    app = Dash(__name__)
    app.layout = html.Div([
        panel_info
    ])
    app.run(debug=True)