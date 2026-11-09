"""Página resumida de resultados y comparación de modelos."""

from dash import html
import plotly.graph_objects as go
from estilo import aplicar_formato, formato_numero, AZUL_OSCURO, AZUL, TURQUESA

RESULTADOS = {
    "Regresión logística": {
        "Accuracy": 0.6978, "Precision": 0.6686, "Recall": 0.6463,
        "F1-score": 0.6573, "ROC-AUC": 0.7567,
    },
    "Random Forest": {
        "Accuracy": 0.6963, "Precision": 0.6766, "Recall": 0.6184,
        "F1-score": 0.6462, "ROC-AUC": 0.7571,
    },
    "XGBoost": {
        "Accuracy": 0.7012, "Precision": 0.6762, "Recall": 0.6403,
        "F1-score": 0.6578, "ROC-AUC": 0.7616,
    },
}

def layout():
    modelos = list(RESULTADOS.keys())
    metricas = list(next(iter(RESULTADOS.values())).keys())

    encabezado = html.Tr([
        html.Th("Métrica"),
        *[html.Th(modelo) for modelo in modelos],
    ])
    filas = [
        html.Tr([
            html.Th(metrica),
            *[
                html.Td(formato_numero(RESULTADOS[modelo][metrica], 4))
                for modelo in modelos
            ],
        ])
        for metrica in metricas
    ]

    tabla = html.Table(
        [html.Thead(encabezado), html.Tbody(filas)],
        style={
            "width": "100%", "borderCollapse": "collapse",
            "textAlign": "center", "marginTop": "14px",
        },
    )

    colores = [AZUL_OSCURO, AZUL, TURQUESA]
    tarjetas = []
    textos = [
        ("XGBoost", "Mayor Accuracy, F1-score y ROC-AUC."),
        ("Regresión logística", "Mayor Recall: identifica una mayor proporción de casos reales de riesgo."),
        ("Random Forest", "Mayor Precision: mayor proporción de alertas correctas."),
    ]
    for (titulo, descripcion), color in zip(textos, colores):
        tarjetas.append(html.Div([
            html.H4(titulo, style={"color": color, "marginBottom": "6px"}),
            html.P(descripcion),
        ], style={
            "backgroundColor": "#F2F6F8", "padding": "14px",
            "borderRadius": "8px", "flex": "1", "minWidth": "190px",
        }))

    return html.Div([
        html.Div([
            html.H1("Resultados y comparación de modelos"),
            html.P(
                "Desempeño de los tres modelos en la identificación de estudiantes "
                "con riesgo de no ingresar a educación superior."
            ),
        ]),
        html.Div([
            html.H2("Comparación de métricas"),
            tabla,
        ], style={
            "backgroundColor": "white", "padding": "20px",
            "borderRadius": "10px", "marginTop": "16px",
        }),
        html.Div([
            html.H2("Principales resultados"),
            html.Div(tarjetas, style={
                "display": "flex", "gap": "12px", "flexWrap": "wrap",
            }),
        ], style={
            "backgroundColor": "white", "padding": "20px",
            "borderRadius": "10px", "marginTop": "16px",
        }),
        html.Div([
            html.Div([
                html.H3("Curvas ROC"),
                html.Img(
                    src="/assets/modelos/07_comparacion_curvas_roc.png",
                    style={"width": "100%"},
                ),
            ], style={
                "backgroundColor": "white", "padding": "16px",
                "borderRadius": "10px", "flex": "1", "minWidth": "300px",
            }),
            html.Div([
                html.H3("Evaluación de umbrales"),
                html.Img(
                    src="/assets/modelos/08_comparacion_umbrales_alertas.png",
                    style={"width": "100%"},
                ),
            ], style={
                "backgroundColor": "white", "padding": "16px",
                "borderRadius": "10px", "flex": "1", "minWidth": "300px",
            }),
        ], style={
            "display": "flex", "gap": "16px", "flexWrap": "wrap",
            "marginTop": "16px",
        }),
        html.P(
            "En XGBoost, bajar el umbral de 0,50 a 0,35 elevó el Recall "
            "de 64,03 % a 80,6 %, pero redujo la precisión. "
            "Resultados de la evaluación inicial documentada en el notebook.",
            style={
                "fontSize": "13px", "padding": "12px",
                "backgroundColor": "#EEF6F6",
                "borderLeft": f"3px solid {TURQUESA}",
                "marginTop": "14px",
            },
        ),
    ], style={"maxWidth": "1200px", "margin": "0 auto"})
