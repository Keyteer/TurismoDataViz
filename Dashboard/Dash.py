# -*- coding: utf-8 -*-
'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ CARGA LIBRERIAS -+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''

import dash
from dash import html, dcc
from dash.dependencies import Input, Output

from utils.cargarDataframes import df1
from plots.plot1 import generar_plot1
from utils.traducirPais import traducir_pais, traducir_pais_inverso


'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ CARGA DATAFRAMES -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''

df = df1()


'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ INICIALIZAR APP -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+###
'''################################################################################################'''

app = dash.Dash(__name__)
app.title = "Dashboard Turismo y PIB"


'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ LAYOUT -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''

app.layout = html.Div([
    html.H1("Dashboard Interactivo: Turismo y PIB", style={"textAlign": "center"}),


###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ PLOT 1 -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
    html.Label("Selecciona un país:"),
    dcc.Dropdown(
    id="dropdown-pais",
    options=[
        {"label": nombre, "value": nombre}
        for nombre in sorted(df["Nombre Español"].dropna().unique())
    ],
    value="Maldivas",
    clearable=False
),
    html.Label("¿Apilar gráfico PIB y Turismo?"),
    dcc.Checklist(
        id="check-apilar",
        options=[{"label": "Apilar", "value": "apilar"},],
        value=["apilar"],  # Por defecto true
        style={"marginBottom": "20px"}
    ),

    dcc.Graph(id="grafico-turismo-pib")
])

###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- CALLBACKS -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
@app.callback(
    Output("grafico-turismo-pib", "figure"),
    Input("dropdown-pais", "value"),
    Input("check-apilar", "value")
)
def actualizar_plot1(pais, apilar_valores):
    apilar = "apilar" in apilar_valores
    return generar_plot1(df, pais, apilar=apilar)





'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ EJECUTAR APP -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''
if __name__ == "__main__":
    app.run(debug=True)