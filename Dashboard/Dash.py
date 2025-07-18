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
from plots.plot3 import generar_plot3, plot3_indicadores
from plots.plot4 import generar_plot4, plot4_indicadores
from plots.plot5 import generar_plot5, plot5_indicadores
from plots.plot6 import generar_plot6, plot6_indicadores
from plots.plot7 import generar_plot7, plot7_indicadores
from plots.panelinfo import generar_panel_info
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

    dbc.Row([
        dbc.Col([
    ###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- PLOT 4 y 6  -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+###
            html.Div(
                id="plot4-6-container",
                # style={"margin": "auto", "padding": "10px", "width": "490px", "height": "450px"},
                children=[
                    dbc.Row([
                        # TITULOS
                        dbc.Col(html.H4(id="titulo-plot6", style={"textAlign": "center"}), width=6),
                        dbc.Col(html.H4(id="titulo-plot4", style={"textAlign": "center"}), width=6),
                    ], className="mb-2"),

                    dbc.Row([
                        # DROPDOWNS
                        dbc.Col(
                            dcc.Dropdown(
                                id="dropdown-indicador-plot6",
                                value="receipts_exports",
                                clearable=False,
                                style={"whiteSpace": "normal"}
                            ), width=6
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="dropdown-indicador-plot4",
                                value="arrivals",
                                clearable=False,
                                style={"whiteSpace": "normal"}
                            ), width=6
                        ),
                    ], className="mb-3"),

                    dbc.Row([
                        # TABLA PLOT 6 + GRAFICO PLOT 4
                        dbc.Col(html.Div(id="tabla-plot6", style={
                            "height": "250px", "overflowY": "auto"
                        }), width=6),

                        dbc.Col(dcc.Graph(id="grafico-plot4", style={
                            "height": "250px", "overflowY": "auto", "justify": "center"
                        }), width=6),
                    ], className="mb-4"),

                    dbc.Row([
                        dbc.Col([
                            html.Label(id="label-rango-anios-plot4"),
                            dcc.RangeSlider(
                                id="rango-anios-plot4",
                                min=1995,
                                max=2022,
                                step=1,
                                value=[2015, 2020],
                                marks={year: str(year) if (year - 1995) % 5 == 0 else "" for year in range(1995, 2023)},
                                tooltip={"placement": "bottom", "always_visible": False},
                                updatemode="drag"
                            )
                        ], width=12)
                    ])
                ]
            ),


    ###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- PLOT 5 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
            html.Div(
                children=[
                    html.H4(id="titulo-plot5", style={"textAlign": "center"}),

                    html.Label(id="label-indicador-x-plot5"),
                    dcc.Dropdown(
                        id="dropdown-indicador-x-plot5",
                        value="GDP",
                        clearable=False,
                        style={"whiteSpace": "normal"}
                    ),

                    html.Label(id="label-indicador-y-plot5"),
                    dcc.Dropdown(
                        id="dropdown-indicador-y-plot5",
                        value="receipts_exports",
                        clearable=False,
                        style={"whiteSpace": "normal"}
                    ),
                    html.Div(id="plot5-aviso-repetido"),

                    html.Label(id="label-rango-anios-plot5"),
                    dcc.RangeSlider(
                        id="rango-anios-plot5",
                        min=1995,
                        max=2022,
                        step=1,
                        value=[2015, 2020],
                        marks={year: str(year) if (year - 1995) % 5 == 0 else "" for year in range(1995, 2023)},
                        tooltip={"placement": "bottom", "always_visible": False},
                        updatemode="drag",
                    ),

                    dbc.Row(children=[
                        dbc.Col(html.Label(id="label-filtrar-topn-plot5"), width="auto"),
                        dbc.Col(
                            dcc.Input(
                                id="input-filtrar-topn-plot5",
                                type="number",
                                min=0,
                                max=100,
                                step=1,
                                value=0,
                                # style={"width": "80px", "textAlign": "center"}
                            ),
                            width="auto"
                        ),
                    ], className="mb-3", justify="center", style={"textAlign": "center"}),

                    dcc.Graph(
                        id="grafico-plot5",
                        # style={"height": "600px", "width": "600px", "overflowY": "scroll", "justify": "center"}
                    )
                ],

                id="plot5",

                # style={"maxWidth": "650px", "margin": "auto", "padding": "20px"}
            ),
        ], width=3, style={"textAlign": "center"}),

        dbc.Col([
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

                style={"maxWidth": "900px", "heigth": 3}  # "margin": "auto", "padding": "20px"}
            ),
            dbc.Row([
                dbc.Col([
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- PANEL INFO +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
                    html.Div([
                        html.Label(id="label-seleccion-pais"),
                        dcc.RangeSlider(
                                        id="rango-anios-panel",
                                        min=1995,
                                        max=2022,
                                        step=1,
                                        value=[2015, 2020],
                                        marks={year: str(year) if (year - 1995) % 10 == 0 else "" for year in range(1995, 2023)},
                                        tooltip={"placement": "bottom", "always_visible": False},
                                        updatemode="drag"
                        ),
                        html.Div(
                            id="panel-info",
                            # style={"height": "300px", "width": "300px", "justify": "center"}
                        )
                    ]),
                ], width=5),
                dbc.Col([

###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- PLOT 3 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
                    html.Div(
                        children=[
                            html.H4(id="titulo-plot3", style={"textAlign": "center"}),

                            html.Label(id="label-indicador-y-plot3"),
                            dcc.Dropdown(
                                id="dropdown-indicador-plot3",
                                options=plot3_indicadores(),
                                value="arrivals",
                                clearable=False,
                                style={"whiteSpace": "normal"}
                            ),

                            html.Label(id="label-seleccion-anio-plot3"),
                            dbc.Row(children=[
                                dbc.Col([
                                    dcc.RangeSlider(
                                        id='rango-anios-plot3',
                                        min=1995,
                                        max=2020,
                                        step=1,
                                        value=[2002, 2003],
                                        marks={year: str(year) if (year - 1995) % 5 == 0 else "" for year in range(1995, 2023)},
                                        tooltip={"placement": "bottom", "always_visible": False},
                                        updatemode="drag"
                                    )
                                ], width=12)
                            ]),

                            dcc.Graph(id="grafico-plot3")
                        ],

                        id="plot3",

                        # style={"maxWidth": "900px", "margin": "auto", "padding": "20px"}
                    ),


                ], width=5)
            ], className="mb-3", justify="center", style={"textAlign": "center"}),
        ], width=6, style={"textAlign": "center"}),

        dbc.Col([
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ Seleccionar país +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
            html.Label(id="label-seleccion-pais"),
            dcc.Dropdown(
                id="dropdown-pais",
                value="MDV",
                clearable=False
            ),

###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- PLOT 7 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
            html.Div(
                children=[
                    html.H4(id="titulo-plot7", style={"textAlign": "center"}),

                    html.Label(id="label-indicador-plot7"),
                    dcc.Dropdown(
                        id="dropdown-indicador-plot7",
                        value="arrivals",
                        clearable=False,
                        style={"whiteSpace": "normal"}
                    ),

                    dcc.Graph(id="grafico-plot7")
                ],

                id="plot7",

                style={"maxWidth": "900px", "margin": "auto", "padding": "20px"}
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

        ], width=3)
    ]),

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

#PLOT 3
@app.callback(
    Output("grafico-plot3", "figure"),
    Output("titulo-plot3", "children"),
    Output("dropdown-indicador-plot3", "options"),
    Input("dropdown-indicador-plot3", "value"),
    Input("rango-anios-plot3", "value"),
    Input("dropdown-pais", "value"), 
    Input("radio-idioma", "value")
)
def actualizar_plot3(id_indicador_1, radio_anio, pais_codigo, idioma):
    
    id_indicador_2 = "departures"
    
    if id_indicador_1 == "receipts_total":
        id_indicador_2 = "expenditures_total"
    elif id_indicador_1 == "receipts_travel":
        id_indicador_2 = "expenditures_travel"
    elif id_indicador_1 == "receipts_transport":
        id_indicador_2 = "expenditures_transport"

    fig = generar_plot3(df, pais_codigo, id_indicador_1, id_indicador_2, radio_anio, idioma=idioma)
    t = textos.get(idioma)
    return (
        fig,
        t["titulo_plot3"].format(
            indicador_x=t["indicadores_df1"][id_indicador_1],
            indicador_y=t["indicadores_df1"][id_indicador_2],
            pais=pais_codigo
        ),
        plot3_indicadores(idioma),
    )
# PLOT 4
@app.callback(
    Output("grafico-plot4", "figure"),
    Output("titulo-plot4", "children"),
    Output("dropdown-indicador-plot4", "options"),
    Input("dropdown-indicador-plot4", "value"),
    Input("rango-anios-plot4", "value"),
    Input("radio-idioma", "value")
)
def actualizar_plot4(id_indicador, rango_anios, idioma):
    fig = generar_plot4(df, id_indicador, rango_anios, idioma)
    t = textos[idioma]
    return (
        fig,
        t["titulo_plot4"].format(indicador=t["indicadores_df1"][id_indicador]),
        plot4_indicadores(idioma)
    )

# PLOT 6
@app.callback(
    Output("tabla-plot6", "children"),
    Output("titulo-plot6", "children"),
    Output("dropdown-indicador-plot6", "options"),
    Input("dropdown-indicador-plot6", "value"),
    Input("rango-anios-plot4", "value"),
    Input("radio-idioma", "value")
)
def actualizar_plot6(id_indicador, rango_anios, idioma):
    t = textos[idioma]
    tabla = generar_plot6(df, id_indicador, rango_anios, idioma)
    return (
        tabla,
        t["titulo_plot6"].format(indicador=t["indicadores_df1"][id_indicador]),
        plot6_indicadores(idioma)
    )

# PLOT 5
@app.callback(
    Output("grafico-plot5", "figure"),
    Output("titulo-plot5", "children"),
    Output("dropdown-indicador-x-plot5", "options"),
    Output("dropdown-indicador-y-plot5", "options"),
    Output("label-indicador-x-plot5", "children"),
    Output("label-indicador-y-plot5", "children"),
    Output("label-rango-anios-plot5", "children"),
    Output("label-filtrar-topn-plot5", "children"),
    Output("plot5-aviso-repetido", "children"),
    Input("dropdown-indicador-x-plot5", "value"),
    Input("dropdown-indicador-y-plot5", "value"),
    Input("rango-anios-plot5", "value"),
    Input("radio-idioma", "value"),
    Input("input-filtrar-topn-plot5", "value")
)
def actualizar_plot5(id_indicador_x, id_indicador_y, rango_anios, idioma, n):
    t = textos.get(idioma, textos["es"])
    opciones = plot5_indicadores(idioma)
    valores_validos = [opt["value"] for opt in opciones]
    # Defaults por primera carga (solo si son None)
    if id_indicador_x is None:
        id_indicador_x = "GDP"
    if id_indicador_y is None:
        id_indicador_y = "receipts_exports"
    # Validar ambos indicadores
    if id_indicador_x not in valores_validos or id_indicador_x is None:
        id_indicador_x = valores_validos[0]
    if id_indicador_y not in valores_validos or id_indicador_y is None:
        # Elige otro valor diferente de X
        id_indicador_y = next(val for val in valores_validos if val != id_indicador_x)
    # Evitar que sean iguales
    mensaje = None
    if id_indicador_x == id_indicador_y:
        id_indicador_y = next(val for val in valores_validos if val != id_indicador_x)
        mensaje = html.Div(
            t["mensaje_indicadores_iguales"],
            style={"color": "red", "fontWeight": "bold", "marginTop": "1px", "textAlign": "center"}
        )
    #Generar fig
    filter_top = max(0, min(n if n is not None else 0, 50))
    fig = generar_plot5(df, id_indicador_x, id_indicador_y, rango_anios, idioma, filter_top=filter_top)
    titulo = t["titulo_plot5"].format(
        indicador_x=t["indicadores_df1"][id_indicador_x],
        indicador_y=t["indicadores_df1"][id_indicador_y]
    )

    return (
        fig,
        titulo,
        opciones,
        opciones,
        t["label_indicador_x_plot5"],
        t["label_indicador_y_plot5"],
        t["label_rango_anios_plot5"],
        t["label_filtrar_top3_plot5"],
        mensaje
    )

# PANEL INFO
@app.callback(
    Output("panel-info", "children"),
    Input("dropdown-pais", "value"),
    Input("rango-anios-panel", "value"),
    Input("radio-idioma", "value")
)
def actualizar_panel_info(codigo_pais, rango_anios, idioma):
    return generar_panel_info(df, codigo_pais, rango_anios, idioma)

# PLOT 7
@app.callback(
    Output("grafico-plot7", "figure"),
    Output("titulo-plot7", "children"),
    Output("dropdown-indicador-plot7", "options"),
    Input("dropdown-indicador-plot7", "value"),
    Input("dropdown-pais", "value"),
    Input("radio-idioma", "value")
)
def actualizar_plot7(id_indicador, pais_codigo, idioma):
    t = textos.get(idioma, textos["es"])
    fig = generar_plot7(df, id_indicador, pais_codigo, idioma)
    return (
        fig,
        t["titulo_plot7"].format(
            indicador=t["indicadores_df1"][id_indicador],
            pais = pais_codigo
            ),
        plot7_indicadores(idioma)
    )

'''################################################################################################'''
###+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ EJECUTAR APP -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-###
'''################################################################################################'''
if __name__ == "__main__":
    app.run(debug=True)