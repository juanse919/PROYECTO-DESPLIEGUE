"""Tablero "Trayectorias estudiantiles | Saber 11 → Educación Superior".

    pip install -r requirements.txt
    python app.py
y abrir http://127.0.0.1:8050 en el navegador.
"""

from dash import Dash, Input, Output, dcc, html

from paginas import acerca, brechas, resumen, modelos

app = Dash(
    __name__,
    title="Trayectorias estudiantiles",
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

# Páginas del menú lateral: (ruta, nombre, módulo)
PAGINAS = [
    ("/", "Resumen", resumen),
    ("/brechas", "Brechas", brechas),
    ("/acerca", "Acerca del proyecto", acerca),
    ("/modelos", "Resultados de modelos", modelos),
]


def menu_lateral() -> html.Div:
    return html.Div(
        className="menu",
        children=[
            html.Div(
                className="marca",
                children=[html.Div("%", className="marca-icono"), html.Span("Trayectorias")],
            ),
            html.Nav(
                [
                    dcc.Link(nombre, href=ruta, id=f"enlace-{ruta.strip('/') or 'resumen'}",
                             className="menu-enlace")
                    for ruta, nombre, _ in PAGINAS
                ]
            ),
            html.Div(
                className="menu-pie",
                children="MIAD · Despliegue de soluciones analíticas · 2026",
            ),
        ],
    )


app.layout = html.Div(
    className="contenedor",
    children=[
        dcc.Location(id="url"),
        menu_lateral(),
        html.Main(id="contenido", className="contenido"),
    ],
)


@app.callback(Output("contenido", "children"), Input("url", "pathname"))
def mostrar_pagina(ruta: str):
    for ruta_pagina, _, modulo in PAGINAS:
        if ruta == ruta_pagina:
            return modulo.layout()
    return resumen.layout()


@app.callback(
    [Output(f"enlace-{r.strip('/') or 'resumen'}", "className") for r, _, _ in PAGINAS],
    Input("url", "pathname"),
)
def resaltar_enlace(ruta: str):
    ruta = ruta if ruta in [r for r, _, _ in PAGINAS] else "/"
    return ["menu-enlace activo" if r == ruta else "menu-enlace" for r, _, _ in PAGINAS]


if __name__ == "__main__":
    # host 0.0.0.0 para poder abrirlo desde fuera cuando se ejecute en EC2 o en Docker
    app.run(host="0.0.0.0", port=8050, debug=False)
