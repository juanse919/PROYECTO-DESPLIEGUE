"""Página Acerca del proyecto."""

from dash import html


def layout() -> html.Div:
    """Presentar el contexto, propósito y alcance del tablero."""
    return html.Div([
        html.Div(className="encabezado", children=[
            html.H1("Acerca del proyecto"),
            html.P(
                "Trayectorias estudiantiles: del examen Saber 11 al ingreso "
                "a la educación superior."
            ),
        ]),
        html.Div(className="tarjeta", children=[
            html.H3("Contexto"),
            html.P(
                "El tránsito entre la educación media y la educación superior "
                "es una etapa clave de la trayectoria educativa. No todos los "
                "estudiantes tienen las mismas condiciones ni las mismas "
                "oportunidades para continuar sus estudios."
            ),
            html.H3("Propósito"),
            html.P(
                "Describir las trayectorias de ingreso a la educación superior "
                "e identificar diferencias entre grupos de estudiantes, con el "
                "fin de aportar evidencia que apoye la comprensión del problema "
                "y la focalización de iniciativas de acceso."
            ),
            html.H3("Alcance"),
            html.P(
                "El tablero presenta indicadores agregados de ingreso observado, "
                "evolución por cohortes y brechas asociadas a características "
                "individuales, familiares y del establecimiento educativo. Los "
                "resultados son descriptivos y dependen de la información "
                "disponible en los archivos de análisis."
            ),
            html.H3("Fuentes y datos"),
            html.P(
                "Se utilizan los resúmenes generados durante la exploración de "
                "la base del proyecto, que reúne 7.138.927 registros. Para "
                "facilitar la consulta web, el tablero utiliza archivos CSV "
                "agregados en lugar de cargar la base completa."
            ),
            html.H3("Metodología"),
            html.P(
                "Las tasas de ingreso se calculan a partir de la proporción de "
                "estudiantes que registran ingreso a educación superior dentro "
                "de cada categoría. Para las cohortes también se diferencia el "
                "ingreso observado del ingreso dentro de una ventana de "
                "seguimiento de cinco años."
            ),
            html.H3("Consideraciones de interpretación"),
            html.P(
                "Las diferencias presentadas no deben interpretarse "
                "automáticamente como efectos causales. Los indicadores "
                "agregados describen patrones del conjunto analizado y no "
                "sustituyen la evaluación individual de cada estudiante."
            ),
        ]),
    ])
