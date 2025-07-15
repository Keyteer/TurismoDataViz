# -*- coding: utf-8 -*-
'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ CARGA LIBRERIAS -+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from utils.cargarDataframes import df1
from plots.plot1 import generar_plot1
from utils.textos_idioma import textos


'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ CARGA DATAFRAMES -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''

df = df1()


'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ INICIALIZAR APP -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+###
'''################################################################################################'''

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard Turismo y PIB"


'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ LAYOUT -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''

app.layout = html.Div([

###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- Título y Botón Ajustes Dashboard +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
    dbc.Row(children =[
        dbc.Col(html.H1(id="titulo-dashboard"), width=True, style={"textAlign": "center"}),
        dbc.Col(
            dbc.Button("ajustes", id="btn-ajustes", n_clicks=0, color="secondary", size="sm"),
            width="auto", style={"textAlign": "right"}
        )
    ], align="center", className="mb-3"),


###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- Modal de Ajustes +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Ajustes del Dashboard")),
            dbc.ModalBody([
                html.Label(id="label-idioma"),
                dcc.RadioItems(
                    id="radio-idioma",
                    options=[
                        {"label": " Español", "value": "es"},
                        {"label": " English", "value": "en"}
                    ],
                    value="es",
                    labelStyle={"display": "block"}
                ),
            ]),
            dbc.ModalFooter(
                dbc.Button(id="cerrar-modal", className="ms-auto", n_clicks=0)
            ),
        ],
        id="modal-ajustes",
        is_open=False,
    ),

###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ Seleccionar país +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
    html.Label(id="label-seleccion-pais"),
    dcc.Dropdown(
        id="dropdown-pais",
        value="MDV",
        clearable=False
    ),

###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- PLOT 1 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
    html.Label(id="label-apilar"),
    dcc.Checklist(
        id="check-apilar",
        options=[{"label": "Apilar", "value": "apilar"},],
        value=["apilar"],  # Por defecto true
        style={"marginBottom": "20px"}
    ),

    dcc.Graph(id="grafico-turismo-pib")
])

###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- CALLBACKS -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
# BOTON AJUSTES
@app.callback(
    Output("modal-ajustes", "is_open"),
    Input("btn-ajustes", "n_clicks"),
    Input("cerrar-modal", "n_clicks"),
    prevent_initial_call=True
)
def toggle_modal(n_abrir, n_cerrar):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    return trigger_id == "btn-ajustes"

# IDIOMA
@app.callback(
    Output("titulo-dashboard", "children"),
    Output("label-seleccion-pais", "children"),
    Output("label-apilar", "children"),
    Output("btn-ajustes", "children"),
    Output("label-idioma", "children"),
    Output("cerrar-modal", "children"),
    Output("dropdown-pais", "options"),
    Input("radio-idioma", "value")
)
def actualizar_textos_y_options(idioma):
    t = textos.get(idioma, textos["es"])
    if idioma == "es":
        opciones = [
            {"label": f"{row['Nombre Español']} ({row['Country Code']})", "value": row["Country Code"]}
            for _, row in df.drop_duplicates(subset="Nombre Español").iterrows()
        ]
    else:
        opciones = [
            {"label": f"{row['Country Name']} ({row['Country Code']})", "value": row["Country Code"]}
            for _, row in df.drop_duplicates(subset="Country Name").iterrows()
        ]
    return (
        t["titulo"],
        t["seleccion_pais"],
        t["apilar"],
        t["ajustes"],
        t["idioma_label"],
        t["cerrar"],
        opciones
    )

# PLOT 1
@app.callback(
    Output("grafico-turismo-pib", "figure"),
    Input("dropdown-pais", "value"),
    Input("radio-idioma", "value"),
    Input("check-apilar", "value")
)
def actualizar_plot1(pais_codigo, idioma, apilar_valores):
    apilar = "apilar" in apilar_valores
    return generar_plot1(df, pais_codigo, apilar=apilar, idioma=idioma)





'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ EJECUTAR APP -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''
if __name__ == "__main__":
    app.run(debug=True)