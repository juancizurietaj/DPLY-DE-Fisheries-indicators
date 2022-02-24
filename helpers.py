import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, State, html, dash_table
import dash
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import csv
import os
# from PIL import Image


# Data loading
data_prices = pd.read_feather(
    "https://raw.githubusercontent.com/juancizurietaj/opendata/main/data_prices_unpivot.feather")
data_captures = pd.read_feather(
    "https://raw.githubusercontent.com/juancizurietaj/opendata/main/data_captures_unpivot.feather")
data_income = pd.read_feather(
    "https://raw.githubusercontent.com/juancizurietaj/opendata/main/data_income_unpivot.feather")
data_controls = pd.read_feather("https://raw.githubusercontent.com/juancizurietaj/opendata/main/data_filters.feather")

# Colors
color_gradients = ["rgb(57, 73, 155)", "rgb(87, 72, 157)", "rgb(112, 70, 157)", "rgb(134, 68, 156)",
                   "rgb(155, 65, 151)", "rgb(174, 62, 146)", "rgb(191, 59, 138)", "rgb(206, 59, 129)",
                   "rgb(219, 61, 118)", "rgb(229, 66, 107)", "rgb(237, 74, 95)", "rgb(243, 84, 83)", "rgb(246, 96, 70)",
                   "rgb(246, 109, 56)", "rgb(244, 123, 41)"]


# Layout sections
# Methods

methods_text_1 = "¿De dónde provienen estos datos?"
methods_text_2 = "Condimentum vitae sapien pellentesque habitant morbi. Convallis posuere morbi leo urna molestie at. Semper quis lectus nulla at volutpat diam ut venenatis tellus. Netus et malesuada fames ac turpis. Ut enim blandit volutpat maecenas volutpat blandit."
methods_text_3 = "Ullamcorper malesuada proin libero nunc consequat interdum varius. Ut placerat orci nulla pellentesque dignissim enim sit amet. Commodo elit at imperdiet dui accumsan sit amet nulla facilisi. Convallis convallis tellus id interdum velit laoreet id"

methods = dbc.Card(
    html.Div(
        [
            html.H1("Ingresos y capturas de recursos pesqueros", className="h1"),
            html.P(methods_text_1, className="labels", style={"padding": "0px 20px"}),
            html.P(methods_text_2, className="texts"),
            html.P(methods_text_3, className="texts"),
            html.Div([
                html.Div([
                    html.Label("Pesquerías monitoreadas", className="labels"),
                    html.P(len(data_prices["pesquería"].dropna().unique()), className="value-cards-value")
                ], style={"display": "flex", "flex-direction": "column"}),
                html.Div([
                    html.Label("Especies monitoreadas", className="labels"),
                    html.P(len(data_prices["especie"].dropna().unique()), className="value-cards-value")
                ], style={"display": "flex", "flex-direction": "column"}),
                html.Div([
                    html.Label("Años con información", className="labels"),
                    html.P(len(data_prices["year"].dropna().unique()), className="value-cards-value")
                ], style={"display": "flex", "flex-direction": "column"}),
                html.Div([
                    html.Label("Indicadores monitoreados", className="labels"),
                    html.P("3", className="value-cards-value")
                ], style={"display": "flex", "flex-direction": "column"})
            ], style={"display": "flex", "flex-direction": "row", "justify-content": "space-around"})
        ]
    ), className="methods-card-box"
)


header = html.Div(
    [
        html.Img(src=r"./assets/de_logo.png",
                 width="130px",
                 style={'display': 'inline-block', "padding": "10px"}),
        html.H4("Ingresos y capturas de recursos pesqueros",
                style={'display': 'inline-block', "color": "white", 'marginLeft': 30, "bottom": 0})
    ], style={"background": "#333f54", 'display': 'inline-block', "width": "100%"}
)

footer = html.Div(
    [
        html.Div(
            [
                html.Img(src="assets/BID.png",
                         height="60px",
                         style={"padding": "0px 15px", "display": "inline-block", "margin-top": "0px"}),
                html.P("Descripción del proyecto donde se enmarcan los datos, créditos a instituciones participantes.",
                       className="footer-grant")
            ]
        ),
        html.Div(
            [
                html.Img(src="assets/edit_dpng_fcd.png",
                         height="85px",
                         style={"padding": "0px 15px", "display": "inline-block", "margin-top": "0px"}),
                html.P("©Dirección del Parque Nacional Galápagos y Fundación Charles Darwin", className="footer-fcd"),
                html.P("Creado por el Departamento de Tecnologías, Información, Investigación y Desarrollo (TIID)",
                       className="footer-tiid")
            ], style={"text-align": "right"}
        )
    ], style={"display": "flex", "justify-content": "space-between", "padding": ""}
)


def create_download_cards(iconA, labelA, textA, buttonA, iconB, textB, labelB, buttonB, iconC, labelC, textC, buttonC):
    downloads = html.Div(
        [
            dbc.Card([html.Div(html.Img(src=iconA, height=50), className="downloads-card-item"),
                      html.Div(html.Label(labelA, className="labels"),
                               className="downloads-card-item"),
                      html.Div(html.P(textA),
                               className="downloads-card-item"),
                      html.Div(dbc.Button(buttonA, size="m"), className="downloads-card-item")],
                     body=True, className="downloads-card-container"),
            dbc.Card([html.Div(html.Img(src=iconB, height=50), className="downloads-card-item"),
                      html.Div(html.Label(labelB, className="labels"),
                               className="downloads-card-item"),
                      html.Div(html.P(textB),
                               className="downloads-card-item"),
                      html.Div(dbc.Button(buttonB, size="m"), className="downloads-card-item")],
                     body=True, className="downloads-card-container"),
            dbc.Card([html.Div(html.Img(src=iconC, height=50), className="downloads-card-item"),
                      html.Div(html.Label(labelC, className="labels"),
                               className="downloads-card-item"),
                      html.Div(html.P(textC),
                               className="downloads-card-item"),
                      html.Div(dbc.Button(buttonC, size="m"), className="downloads-card-item")],
                     body=True, className="downloads-card-container")
        ], className="downloads-container"
    )

    return downloads


# Helper functions
def checklist_creator(df, column, _id):
    unique_values = sorted(df[column].dropna().unique())
    checklist = dbc.Checklist(id=_id,
                              options=[{"label": i, 'value': i} for i in unique_values],
                              value=["Langosta"],
                              switch=True)
    return checklist


def check_all_creator(_id, value):
    check_all = dbc.Checkbox(id=_id,
                             label="Seleccionar todo",
                             value=value)
    return check_all


def tab_creator(label_name, content):
    tab = dbc.Tab(content, label=label_name,
                  tab_style={'backgroundColor': '#e9ebef'},
                  active_label_style={'color': '#333f54', 'fontWeight': 'bold'},
                  label_style={'color': 'gray'})
    return tab


def create_line_chart(df, x, y, color, log_plot_value, header_metric, years_min, years_max, prefix, suffix):
    fig = px.line(data_frame=df,
                  x=x,
                  y=y,
                  log_y=log_plot_value,
                  color=color,
                  markers=True,
                  line_shape="spline",
                  color_discrete_sequence=color_gradients)
    # Shuffle colors: random.sample(color_gradients, len(color_gradients))

    header = "<b>" + header_metric + " por " + color + " </b><br>"
    description = "<i> Valores del periodo entre " + years_min + " y " + years_max + "</i>"

    fig.update_layout(title=(header + description),
                      plot_bgcolor="#ecf3f6",
                      hoverlabel_namelength=35,
                      hovermode="x",
                      title_font_family="Roboto",
                      title_font_color="#333f54")

    fig.update_traces(mode="markers+lines", hovertemplate=prefix + "%{y:.2f}" + suffix)

    return fig


def create_table_header():
    headers = html.Div(
        id="table-header",
        children=[
            # html.Label(header, className="labels"),
            # html.P(description, style={"fontStyle": "italic"})
        ]
    )
    return headers


def create_table_elements(df, values, array_for_index, columns, agg_func, metric, year_min, year_max):
    df = pd.pivot_table(data=df,
                        values=values,
                        index=array_for_index,
                        columns=columns,
                        aggfunc=agg_func)

    df.reset_index(inplace=True)
    data_for_table = df.round(2).to_dict(orient="records")
    columns_for_table = [{"name": i, "id": i} for i in df.columns]

    if len(array_for_index) > 1:
        header = metric + " por " + array_for_index[0] + " y por " + array_for_index[1]
    else:
        header = metric + " por " + array_for_index[0]

    header_for_table = [
        html.Label(header, className="labels"),
        html.P("Valores del periodo entre " + year_min + " y " + year_max, style={"fontStyle": "italic"})]

    return data_for_table, columns_for_table, header_for_table


def create_table():
    table = dash_table.DataTable(
        id='table',
        data=[],
        sort_action='native',
        style_table={'overflowX': 'auto'},
        style_header={
            "backgroundColor": "#333f54",
            "fontWeight": "bold",
            "color": "white",
        },
        style_cell={'textAlign': 'center',
                    'font-family': 'sans-serif',
                    'fontSize': 12},
        style_data_conditional=[
            {
                "if": {"state": "selected"},
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid #333f54",
            }
        ]
    )

    return table


def create_sparkline(df, groupby_col, values):

    df_to_sparkline = df.groupby([groupby_col])[values].mean()
    df_to_sparkline = round(df_to_sparkline, 2)

    if len(df_to_sparkline) > 0:
        start_value = df_to_sparkline[1]
        end_value = df_to_sparkline[-1]
    else:
        start_value, end_value = 0, 0

    fig = px.line(df_to_sparkline, height=70, width=150, markers=True)
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_traces(line_color="#929AA9",
                      line_width=3,
                      # mode="markers+lines",
                      hovertemplate=None)
    fig.update_layout(annotations=[],
                      overwrite=True,
                      showlegend=False,
                      plot_bgcolor="white",
                      margin=dict(t=10, l=10, b=10, r=10),
                      hovermode="closest")

    fig.add_trace(go.Indicator(
        mode="delta",
        value=end_value,
        delta={"reference": start_value,
               "valueformat": ".0%",
               "relative": True,
               "position": "bottom",
               "increasing.color": "#333f54",
               "decreasing.color": "#F47B29"},
        domain={'y': [0, 0.7], 'x': [0, 1]}
    ))

    return fig


def create_citation(header, grouping_text, fisheries_array, year_min, year_max, fig_or_table):
    a = "Fundación Charles Darwin. 2022. " + \
        header + grouping_text + " para"
    b = ", ".join(fisheries_array)
    b = b.replace("[", "").replace("]", "").replace("'", "").lower()
    text = a + " " + b + ". Valores del periodo entre " + year_min + " y " + year_max
    citation = html.Div([html.P("Para citar esta " + fig_or_table, className="citation-header"),
                         html.P(text, className="citation")])

    return citation



iconA = "assets/icon_metadata.png"
labelA = "Descarga de metadatos"
textA = "Los metadatos son 'datos acerca de los datos'. Describen el contenido, la calidad, el formato y otras características de este conjuntos de los datos. También incluyen las formas de citación, créditos y licencias de los datos."
buttonA = "Descargar metadatos"

iconB = "assets/icon_dix.png"
labelB = "Descarga de diccionario de datos"
textB = "Es el significado de cada una de los 'campos' o 'variables' del conjunto de datos. Muestra el significado de cada encabezado del conjunto de datos y la descripción de los datos que contiene."
buttonB = "Descargar diccionario de datos"

iconC = "assets/icon_data.png"
labelC = "Descarga los datos abiertos"
textC = "Los datos abiertos son el conjunto de datos detrás de este Data Explorer. Tienen un formato tabular (.csv) y muestran los datos en su forma más desagregada."
buttonC = "Descargar los datos abiertos"

downloads = create_download_cards(iconA, labelA, textA, buttonA, iconB, textB, labelB, buttonB, iconC, labelC, textC,
                                  buttonC)
