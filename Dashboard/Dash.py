# -*- coding: utf-8 -*-
'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ CARGA LIBRERIAS -+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''

import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc

from utils.cargarDataframes import df1, load_arrivals_df
from plots.plot1 import generar_plot1
from plots.plot2 import generar_plot2
from plots.plot4 import generar_plot4, opciones_dropdown_indicadores
from utils.textos_idioma import textos


'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ CARGA DATAFRAMES -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''

df = df1()
arrivals_df = load_arrivals_df()


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
    html.Div(
        children=[
            html.H4(id="titulo-plot1", style={"textAlign": "center"}),

            dbc.Row(children=[
                dbc.Col(html.Label(id="label-apilar"), width="auto"),
                dbc.Col(
                    dcc.Checklist(
                        id="check-plot1",
                        options=[],
                        value=["apilar"],
                        inline=True,
                        style={"marginBottom": "0px"}
                    ),
                    width="auto"
                ),
            ], className="mb-3", justify="center", style={"textAlign": "center"}),

            dcc.Graph(id="grafico-turismo-pib")
        ],

        id="plot1",

        style={"maxWidth": "900px", "margin": "auto", "padding": "20px"}
    ),


###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- PLOT 2 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
    html.Div(
        children=[
            html.H4(id="titulo-plot2", style={"textAlign": "center"}),

            dbc.Row(children=[
                dbc.Col(html.Label(id="label-anio-plot2"), width="auto", style={"textAlign": "left"}),
                dbc.Col(
                    dcc.Slider(
                        id='slider-plot2',
                        min=int(arrivals_df.columns[1]),
                        max=int(arrivals_df.columns[-1]),
                        value=2008,
                        marks={
                            int(a): str(a) if i % 3 == 0 else "" # Mostrar cada 3 años
                            for i, a in enumerate(arrivals_df.columns[1:])
                        },
                        step=1,  # Permite seleccionar solo los años disponibles
                        included=False,  # Eliminar rango
                        tooltip={"placement": "bottom", "always_visible": False},
                        updatemode="drag",  # Para actualizar al arrastrar
                    ),
                    width=True, style={"textAlign": "center"}
                ),
            ], className="mb-3", justify="center", style={"textAlign": "center"}),

            html.Iframe(id="mapa-plot2", srcDoc=None, width="100%", height="600px", style={"display": "block"})
        ],

        id="plot2",

        style={"maxWidth": "900px", "margin": "auto", "padding": "20px"}
    ),
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- PLOT 4 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
    html.Div(
        children=[
            html.H4(id="titulo-plot4", style={"textAlign": "center"}),

            html.Label(id="label-indicador-plot4"),

            dcc.Dropdown(
                id="dropdown-indicador-plot4",
                value="arrivals",
                clearable=False,
                style={"whiteSpace": "normal"}
            ),

            html.Label(id="label-rango-anios-plot4"),

            dcc.RangeSlider(
                id="rango-anios-plot4",
                min=1995,
                max=2022,
                step=1,
                value=[2015, 2020],
                marks={
                    year: str(year) if (year - 1995) % 5 == 0 else ""
                    for year in range(1995, 2023)
                },
                tooltip={"placement": "bottom", "always_visible": False},
                updatemode="drag",  # Para actualizar al arrastrar
            ),

            dcc.Graph(id="grafico-plot4", style={"height": "300px", "width": "210px",
                                                 "overflowY": "scroll", "justify": "center"})
        ],

        id="plot4",

        style={"maxWidth": "210px", "margin": "auto", "padding": "20px"}
    )
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
    Output("check-plot1", "options"),
    Output("titulo-plot2", "children"),
    Output("label-anio-plot2", "children"),
    Input("radio-idioma", "value")
)
def actualizar_textos_y_options(idioma):
    t = textos.get(idioma, textos["es"])
    if idioma == "es":
        opciones_paises = [
            {"label": f"{row['Nombre Español']} ({row['Country Code']})", "value": row["Country Code"]}
            for _, row in df.drop_duplicates(subset="Nombre Español").iterrows()
        ]
    else:
        opciones_paises = [
            {"label": f"{row['Country Name']} ({row['Country Code']})", "value": row["Country Code"]}
            for _, row in df.drop_duplicates(subset="Country Name").iterrows()
        ]
    check_plot1 = [{
        "label": t["check_apilar"],
        "value": "apilar"
    }]
    return (
        t["titulo"],
        t["seleccion_pais"],
        t["apilar"],
        t["ajustes"],
        t["idioma_label"],
        t["cerrar"],
        opciones_paises,
        check_plot1,
        t["titulo_plot2"],
        t["label_anio_plot2"]

    )

# PLOT 1
@app.callback(
    Output("grafico-turismo-pib", "figure"),
    Output("titulo-plot1", "children"),
    Input("dropdown-pais", "value"),
    Input("radio-idioma", "value"),
    Input("check-plot1", "value")
)
def actualizar_plot1(pais_codigo, idioma, apilar_valores):
    apilar = "apilar" in apilar_valores
    titulo, fig = generar_plot1(df, pais_codigo, apilar=apilar, idioma=idioma)
    return fig, titulo

# PLOT 2
@app.callback(
    Output("mapa-plot2", "srcDoc"),
    Input("slider-plot2", "value")
)
def actualizar_mapa(anio):
    mapa = generar_plot2(arrivals_df, year=anio)
    mapa.save("plots/plot2.html")
    with open("plots/plot2.html", "r", encoding="utf-8") as f:
        return f.read()

# PLOT 4
@app.callback(
    Output("grafico-plot4", "figure"),
    Output("titulo-plot4", "children"),
    Output("dropdown-indicador-plot4", "options"),
    Output("label-indicador-plot4", "children"),
    Output("label-rango-anios-plot4", "children"),
    Input("dropdown-indicador-plot4", "value"),
    Input("rango-anios-plot4", "value"),
    Input("radio-idioma", "value")
)
def actualizar_plot4(id_indicador, rango_anios, idioma):
    fig = generar_plot4(df, id_indicador, rango_anios, idioma)
    t = textos[idioma]
    return (
        fig,
        t["titulo_plot4"].format(indicador=t["indicadores_plot4"][id_indicador]),
        opciones_dropdown_indicadores(idioma),
        t["label_indicador_plot4"],
        t["label_rango_anios_plot4"]
    )



'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ EJECUTAR APP -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''
if __name__ == "__main__":
    app.run(debug=True)