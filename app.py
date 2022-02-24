from helpers import *

# App constructor
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Server definition
server = app.server

# Controls
fisheries_control = dbc.Checklist(id="fishery-selection",
                                  options=[{"label": i, 'value': i} for i in
                                           sorted(data_controls["pesquería"].dropna().unique())],
                                  value=["Pesca de altura"],
                                  switch=True)

species_control = dbc.Checklist(id="species-selection", switch=True)

controls = html.Div(
    [
        html.Label("Filtros y controles", className="labels"),
        html.Br(),
        html.Br(),
        dbc.Accordion(
            dbc.AccordionItem(
                title="Pesquería",
                children=[
                    check_all_creator("fishery-all-selected", False),
                    fisheries_control
                ]
            ), start_collapsed=False
        ),
        html.Br(),
        dbc.Accordion(
            dbc.AccordionItem(
                title="Especies",
                children=[
                    check_all_creator("species-all-selected", True),
                    species_control
                ]
            ), start_collapsed=True
        )
    ]
)

# Indicators
indicators = html.Div(id="indicators")

# Charts
charts = html.Div(
    children=[
        html.Br(),
        indicators,
        html.Br(),
        html.Div(dbc.Checkbox(id="log-plot",
                              label="Mostrar eje Y en escala logarítmica",
                              value=False),
                 className="y-log-check"),
        dcc.Graph(id="chart", config={'displayModeBar': False}),
        html.Div(id="fig-citation"),
        html.Br(),
        html.Button(children=["Descargar imagen",
                              dbc.Spinner(html.Div(id="loading-image"),
                                          color="white",
                                          spinner_style={"width": "2rem", "height": "2rem", "margin-top": "0px"})],
                    id="btn-image",
                    n_clicks=0,
                    className="download-button"),
        html.Div(id="download-container"),
    ]
)

# Tables
tables = html.Div(
    children=[
        create_table_header(),  # id table-header is set inside function
        create_table(),  # id table is set inside function
        html.Br(),
        html.Div(id="table-citation"),
        html.Button(children=["Descargar tabla",
                              dbc.Spinner(html.Div(id="loading-table"),
                                          color="white",
                                          spinner_style={"width": "2rem", "height": "2rem", "margin-top": "0px"})],
                    id="btn-table", n_clicks=0, className="download-button"),
        html.Div(id="download-container-table")
    ], style={"padding": "20px"}
)

# Charts and tables tabs
subtabs = dbc.Tabs([
    tab_creator("GRÁFICO", charts),
    tab_creator("TABLA", tables)])

# Chart controls
chart_controls = html.Div(
    [
        html.Label("Métrica", className="labels"),
        dcc.Dropdown(id="df-selection",
                     options=[{"label": "Precios", "value": "precios"},
                              {"label": "Capturas", "value": "capturas"},
                              {"label": "Ingresos", "value": "ingresos"}],
                     value="precios",
                     clearable=False),
        html.Br(),
        dbc.Checklist(id="show-group-results",
                      options=[{"label": "Mostrar resultados agrupados por pesquería", "value": False}],
                      value=False,
                      switch=True)
    ]
)

# Tab layout: charts
chart_tab_sections = html.Div(
    dbc.Row(
        [
            dbc.Col(dbc.Card(controls, body=True),
                    width=3,
                    style={"marginTop": "20px"},
                    id="controls-col",
                    className="card-box"),
            dbc.Col([dbc.Card(chart_controls, body=True, className="card-box"),
                     html.Br(),
                     dbc.Card(subtabs, body=True, className="card-box-behind")],
                    width=9,
                    style={"marginTop": "20px"},
                    id="charts-col")
        ], style={"display": "flex"}, id="controls"
    )
)

# Tabs
tab1 = tab_creator("MÉTODOS", methods)
tab2 = tab_creator("FIGURAS", chart_tab_sections)
tab3 = tab_creator("DATOS ABIERTOS", downloads)

tabs = dbc.Tabs([tab1, tab2, tab3])

# App layout
app.layout = html.Div(
    [
        header,
        tabs,
        html.Hr(),
        footer
    ], style={"width": "99%"}  # This avoids the horizontal scroll bar
)


# Callbacks
@app.callback(
    Output("download-container", "children"),
    Output("btn-image", "n_clicks"),
    Output("loading-image", "children"),
    Input("btn-image", "n_clicks"),
    Input("chart", "figure")
)
def download_charts(n_clicks, chart_dict):
    file_name = chart_dict["layout"]["title"]["text"]
    idx1 = file_name.index("<b>")
    idx2 = file_name.index("</b>")
    file_name = file_name[idx1 + len("<b>"): idx2] + ".png"
    fig = go.Figure(chart_dict)
    if n_clicks > 0:
        spinner_children = []
        fig.write_image(file_name)
        children = dcc.Download(id="dcc-download", data=dcc.send_file(file_name)), os.remove(file_name)
        n_clicks = 0
        return children, n_clicks, spinner_children
    else:
        spinner_children = []
        children = dcc.Download(id="dcc-download")
        return children, n_clicks, spinner_children


@app.callback(
    Output("download-container-table", "children"),
    Output("btn-table", "n_clicks"),
    Output("loading-table", "children"),
    Input("btn-table", "n_clicks"),
    Input("table", "data"),
    Input("table-header", "children")
)
def download_tables(n_clicks, data_dict, header):
    file_name = header[0]["props"]["children"] + ".csv"
    df = pd.DataFrame.from_dict(data_dict)
    if n_clicks > 0:
        spinner_children = []
        df.to_csv(file_name)
        children = dcc.Download(id="dcc-download-table", data=dcc.send_file(file_name)), os.remove(file_name)
        n_clicks = 0
        return children, n_clicks, spinner_children
    else:
        spinner_children = []
        children = dcc.Download(id="dcc-download")
        return children, n_clicks, spinner_children


@app.callback(
    Output("fishery-selection", "value"),
    Input("fishery-all-selected", "value"),
    prevent_initial_call=True
)
def update_fishery_controls(check):
    fishery_values = []
    if check:
        fishery_values = data_controls["pesquería"].dropna().unique()

    return fishery_values


@app.callback(
    Output("species-selection", "options"),
    Output("species-selection", "value"),
    Input("fishery-selection", "value"),
    Input("species-all-selected", "value"),
)
def update_species_controls(fishery_values, check):
    data_controls_copy = data_controls.copy(deep=True)
    species_options = []
    species_values = []

    if fishery_values:
        df = data_controls_copy[data_controls_copy["pesquería"].isin(fishery_values)]
        species_options = [{"label": i, 'value': i} for i in df["especie"].dropna().unique()]
        species_values = [i["value"] for i in species_options]

    if check:
        species_values = [i["value"] for i in species_options]
    else:
        species_values = []

    return species_options, species_values


@app.callback(
    Output("chart", "figure"),
    Output("table", "data"),
    Output("table", "columns"),
    Output("table-header", "children"),
    Output("indicators", "children"),
    Output("fig-citation", "children"),
    Output("table-citation", "children"),
    Input("df-selection", "value"),
    Input("fishery-selection", "value"),
    Input("species-selection", "value"),
    Input("show-group-results", "value"),
    Input("log-plot", "value"),
)
def generate_figures(df_selection, fishery_selection, species_selection, grouped_by_fishery, log_plot_value):
    if df_selection == "precios":
        df = data_prices
        header_metric = "Precio en USD por libra "
        indicator_prefix = "US$ "
        indicator_suffix = ""

    elif df_selection == "capturas":
        df = data_captures
        header_metric = "Capturas en libras "
        indicator_prefix = ""
        indicator_suffix = " lbs"

    else:
        df = data_income
        header_metric = "Ingresos en USD "
        indicator_prefix = "US$ "
        indicator_suffix = ""

    selections = [fishery_selection, species_selection]
    years_min = df["year"].dropna().unique().min()
    years_max = df["year"].dropna().unique().max()
    df_copy = df.copy(deep=True)
    df_copy["values"] = round(df_copy["values"], 2)

    if selections:
        df_copy = df_copy[
            df_copy["pesquería"].isin(selections[0]) &
            df_copy["especie"].isin(selections[1])
            ]

        fig = create_line_chart(df_copy, "year", "values", "especie", log_plot_value, header_metric, years_min,
                                years_max, indicator_prefix, indicator_suffix)

        data_for_table, columns_for_table, header_for_table = create_table_elements(df_copy,
                                                                                    "values",
                                                                                    ["pesquería", "especie"],
                                                                                    "year",
                                                                                    "sum",
                                                                                    header_metric,
                                                                                    years_min,
                                                                                    years_max)

        indicator_mean = round(df_copy["values"].mean(), 2)
        indicator_median = round(df_copy["values"].median(), 2)
        indicator_sparkline = create_sparkline(df_copy, "year", "values")

        indicator_cards = html.Div(
            [
                html.Div([html.Label("Promedio entre " + years_min + " y " + years_max, className="labels"),
                          html.P(indicator_prefix + str(indicator_mean) + indicator_suffix,
                                 className="value-cards-value")]),
                html.Div([html.Label("Mediana entre " + years_min + " y " + years_max, className="labels"),
                          html.P(indicator_prefix + str(indicator_median) + indicator_suffix,
                                 className="value-cards-value")]),
                html.Div([html.Label("Diferencia " + years_min + " - " + years_max, className="labels"),
                          dcc.Graph(figure=indicator_sparkline,
                                    responsive=False,
                                    config={'displayModeBar': False})])
            ],
            style={"display": "flex", "flex-orientation": "columns", "justify-content": "space-evenly"}
        )

        fig_citation = create_citation(header_metric, "por pesquería y por especie", selections[0], years_min,
                                       years_max, "figura:")
        table_citation = create_citation(header_metric, "por pesquería y por especie", selections[0], years_min,
                                         years_max, "tabla:")

    if grouped_by_fishery:
        if df_selection == "precios":
            df_copy = df_copy.groupby(["pesquería", "year"])["values"].mean()
        else:
            df_copy = df_copy.groupby(["pesquería", "year"])["values"].sum()

        df_copy = pd.DataFrame(df_copy)
        df_copy.reset_index(col_level=0, inplace=True)

        fig = create_line_chart(df_copy, "year", "values", "pesquería", log_plot_value, header_metric, years_min,
                                years_max, indicator_prefix, indicator_suffix)

        data_for_table, columns_for_table, header_for_table = create_table_elements(df_copy,
                                                                                    "values",
                                                                                    ["pesquería"],
                                                                                    "year",
                                                                                    "sum",
                                                                                    header_metric,
                                                                                    years_min,
                                                                                    years_max)

        fig_citation = create_citation(header_metric, "por pesquería", selections[0], years_min, years_max, "figura:")
        table_citation = create_citation(header_metric, "por pesquería", selections[0], years_min, years_max, "tabla:")

    return fig, data_for_table, columns_for_table, header_for_table, indicator_cards, fig_citation, table_citation


if __name__ == '__main__':
    app.run_server(debug=True)
