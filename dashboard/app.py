
# Importar las librerías y páginas del tablero
from dash import Dash, Input, Output, State, dcc, html

from paginas import acerca, brechas, resumen, predicciones


# Crear la aplicación Dash
app = Dash(
    __name__,
    title="Trayectorias estudiantiles",
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

server = app.server


# Registrar el callback de predicciones en la aplicación
app.callback(
    Output("resultado-prediccion", "children"),
    Input("btn-predecir", "n_clicks"),
    [
        State(f"pred-{variable}", "value")
        for variable in list(predicciones.NUMERICAS.keys())
        + list(predicciones.OPCIONES.keys())
    ],
    prevent_initial_call=True
)(predicciones.generar_prediccion)


# Registrar el desplazamiento automático hacia el resultado
app.clientside_callback(
    """
    function(children) {

        if (children) {

            const resultado = document.getElementById(
                "resultado-prediccion"
            );

            if (resultado) {

                window.requestAnimationFrame(function() {

                    resultado.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                });

            }

        }

        return children ? "resultado actualizado" : "";

    }
    """,
    Output("estado-desplazamiento", "data"),
    Input("resultado-prediccion", "children"),
    prevent_initial_call=True
)


# Definir las páginas disponibles en el tablero
PAGINAS = [
    ("/", "Resumen", resumen),
    ("/brechas", "Brechas", brechas),
    ("/predicciones", "Predicciones", predicciones),
    ("/acerca", "Acerca del proyecto", acerca),
]


# Construir el menú lateral
def menu_lateral():

    return html.Div(
        className="menu",
        children=[
            html.Div(
                className="marca",
                children=[
                    html.Div("%", className="marca-icono"),
                    html.Span("Trayectorias")
                ],
            ),

            html.Nav([
                dcc.Link(
                    nombre,
                    href=ruta,
                    id=f"enlace-{ruta.strip('/') or 'resumen'}",
                    className="menu-enlace"
                )
                for ruta, nombre, _ in PAGINAS
            ]),

            html.Div(
                className="menu-pie",
                children="MIAD · Despliegue de soluciones analíticas · 2026",
            ),
        ],
    )


# Construir la estructura principal del tablero
app.layout = html.Div(
    className="contenedor",
    children=[
        dcc.Location(id="url"),
        menu_lateral(),
        html.Main(id="contenido", className="contenido"),
    ],
)


# Mostrar la página seleccionada
@app.callback(
    Output("contenido", "children"),
    Input("url", "pathname")
)
def mostrar_pagina(ruta):

    for ruta_pagina, _, modulo in PAGINAS:
        if ruta == ruta_pagina:
            return modulo.layout()

    return resumen.layout()


# Resaltar el enlace de la página activa
@app.callback(
    [
        Output(f"enlace-{r.strip('/') or 'resumen'}", "className")
        for r, _, _ in PAGINAS
    ],
    Input("url", "pathname"),
)
def resaltar_enlace(ruta):

    ruta = ruta if ruta in [r for r, _, _ in PAGINAS] else "/"

    return [
        "menu-enlace activo" if r == ruta else "menu-enlace"
        for r, _, _ in PAGINAS
    ]


# Ejecutar el tablero
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
