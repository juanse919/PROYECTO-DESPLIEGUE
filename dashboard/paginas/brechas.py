"""Página Brechas (a cargo de Paula Guarín)."""

from dash import html


def layout() -> html.Div:
    return html.Div([
        html.Div(className="encabezado", children=[
            html.H1("Brechas en el ingreso a la educación superior"),
            html.P("Página en construcción."),
        ]),
    ])
