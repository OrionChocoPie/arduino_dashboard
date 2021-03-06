import os

import dash
import dash_auth
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from db import Connector


VALID_USERNAME_PASSWORD_PAIRS = {os.getenv("AUTH_USER"): os.getenv("AUTH_PASSWORD")}
SECONDS_UPDATE_PERIOD = 60
LAST_ELEMS = 100
MEAN_PERIOD = 1

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

connector = Connector()

app.layout = html.Div(
    [
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo.png"),
                            id="plotly-image",
                            style={
                                "margin-top": "25px",
                                "height": "100px",
                                "width": "auto",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Greenhouse",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5("Real Time information from Arduino device", style={"margin-top": "0px"}),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Source Code", id="learn-more-button"),
                            href="https://github.com/OrionChocoPie/arduino_dashboard",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [html.H6(id="temperature"), html.P("?????????????? ??????????????????????, ???")],
                            id="wells",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.H6(id="illumination"), html.P("?????????????? ????????????????????????, %")],
                            id="oil",
                            className="mini_container",
                        ),
                    ],
                    className="row container-display",
                ),
            ],
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [html.H6(id="ground_humidity"), html.P("?????????????? ?????????????????? ??????????, %")],
                            id="gas",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.H6(id="air_humidity"), html.P("?????????????? ?????????????????? ??????????????, %")],
                            id="water",
                            className="mini_container",
                        ),
                    ],
                    className="row container-display",
                ),
            ],
        ),
        html.Div(
            [
                dcc.Graph(
                    id="temperature_graph",
                    config={
                        "displayModeBar": False,
                    },
                )
            ],
            className="pretty_container",
        ),
        html.Div(
            [
                dcc.Graph(
                    id="illumination_graph",
                    config={
                        "displayModeBar": False,
                    },
                )
            ],
            className="pretty_container",
        ),
        html.Div(
            [
                dcc.Graph(
                    id="ground_humidity_graph",
                    config={
                        "displayModeBar": False,
                    },
                )
            ],
            className="pretty_container",
        ),
        html.Div(
            [
                dcc.Graph(
                    id="air_humidity_graph",
                    config={
                        "displayModeBar": False,
                    },
                )
            ],
            className="pretty_container",
        ),
        dcc.Interval(
            id="interval-component",
            interval=SECONDS_UPDATE_PERIOD * 1000,  # in milliseconds
            n_intervals=0,
        ),
    ]
)


def create_graph(title, time_indexes, values):
    layout = dict(
        autosize=True,
        automargin=True,
        margin=dict(l=30, r=30, b=20, t=40),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        legend=dict(font=dict(size=10), orientation="h"),
        title=title,
        showlegend=False,
        xaxis={"fixedrange": True},
        yaxis={"fixedrange": True},
    )

    values = [round(x, 2) for x in values]

    data = [
        dict(
            type="scatter",
            mode="lines+markers",
            name="Gas Produced (mcf)",
            x=time_indexes,
            y=values,
            line=dict(shape="spline", smoothing=2, width=1, color="#92d8d8"),
            marker=dict(symbol="diamond-open"),
        ),
    ]

    figure = dict(data=data, layout=layout)
    return figure


@app.callback(
    [
        Output("temperature", "children"),
        Output("illumination", "children"),
        Output("ground_humidity", "children"),
        Output("air_humidity", "children"),
        Output("temperature_graph", "figure"),
        Output("illumination_graph", "figure"),
        Output("ground_humidity_graph", "figure"),
        Output("air_humidity_graph", "figure"),
    ],
    Input("interval-component", "n_intervals"),
)
def update_info(n):
    # update data
    df = connector.select_values()
    df = df.sort_values("time", ascending=False)
    df = df.iloc[:LAST_ELEMS]

    # update dash
    df.columns = ["time", "??????????????????????, ???", "????????????????????????, %", "?????????????????? ??????????, %", "?????????????????? ??????????????, %"]
    columns = df.columns[1:]

    means = [df.loc[:MEAN_PERIOD, columns].mean() for columns in columns]
    means = [round(x, 2) for x in means]
    graphs = [create_graph(column, df["time"], df[column]) for column in columns]

    return [*means, *graphs]


if __name__ == "__main__":
    app.run_server(debug=True)
