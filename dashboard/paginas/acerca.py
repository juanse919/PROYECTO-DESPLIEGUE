"""Página Acerca del proyecto (a cargo de Paula Guarín)."""

from dash import html


def layout() -> html.Div:
    return html.Div([
        html.Div(className="encabezado", children=[
            html.H1("Acerca del proyecto"),
            html.P("Página en construcción."),
        ]),
    ])
