"""Página Brechas: comparación descriptiva de tasas de ingreso a educación superior."""

import plotly.graph_objects as go
from dash import dcc, html

import datos
from estilo import (
    AZUL, AZUL_OSCURO, GRIS, TURQUESA, TURQUESA_CLARO,
    aplicar_formato, formato_numero,
)


# Cargar los resúmenes agregados disponibles en el proyecto.
ESTRATO = datos.cargar_estrato()
AREA = datos._leer_tasa("cole_area_ubicacion")
INTERNET = datos._leer_tasa("fami_tieneinternet")
COMPUTADOR = datos._leer_tasa("fami_tienecomputador")
EDUCACION_MADRE = datos._leer_tasa("fami_educacionmadre")

# El archivo de deciles tiene una estructura distinta a los demás resúmenes.
from pathlib import Path
import pandas as pd

DECILES = pd.read_csv(datos.RUTA_EXPLORACION / "tasa_decil_matematicas.csv")


def _preparar_si_no(tabla):
    """Asignar etiquetas legibles y excluir categorías sin dato reportado."""
    resultado = tabla.dropna(subset=["categoria"]).copy()
    resultado["categoria"] = resultado["categoria"].map(
        {0: "No", 0.0: "No", 1: "Sí", 1.0: "Sí"}
    )
    return resultado


INTERNET = _preparar_si_no(INTERNET)
COMPUTADOR = _preparar_si_no(COMPUTADOR)
AREA = AREA.dropna(subset=["categoria"]).copy()
AREA["categoria"] = AREA["categoria"].str.capitalize()
EDUCACION_MADRE = EDUCACION_MADRE.dropna(subset=["categoria"]).copy()
EDUCACION_MADRE["categoria"] = EDUCACION_MADRE["categoria"].map(
    {0: "Ninguna", 1: "Primaria", 2: "Secundaria", 3: "Técnica/tecnológica", 4: "Profesional o superior"}
).fillna(EDUCACION_MADRE["categoria"].astype(str))


def _grafica_barras(tabla, columna, titulo_eje="Tasa de ingreso (%)", alto=300):
    """Construir una gráfica horizontal con tasa y número de estudiantes."""
    fig = go.Figure(go.Bar(
        x=tabla["tasa"],
        y=tabla["categoria"],
        orientation="h",
        marker_color=TURQUESA,
        text=[f"{formato_numero(valor, 1)} %" for valor in tabla["tasa"]],
        textposition="outside",
        customdata=tabla["estudiantes"],
        hovertemplate=(
            "%{y}<br>Tasa de ingreso: %{x:.1f} %"
            "<br>Estudiantes: %{customdata:,}<extra></extra>"
        ),
    ))
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(title=titulo_eje, range=[0, 100], ticksuffix=" %")
    return aplicar_formato(fig, alto=alto)


def _grafica_deciles():
    """Mostrar la tasa observada de ingreso según decil de matemáticas."""
    fig = go.Figure(go.Scatter(
        x=DECILES["decil_mat"],
        y=DECILES["enroll_full"],
        mode="lines+markers+text",
        line=dict(color=AZUL, width=3),
        marker=dict(color=TURQUESA, size=9),
        text=[f"{formato_numero(valor, 1)}%" for valor in DECILES["enroll_full"]],
        textposition="top center",
        hovertemplate="Decil %{x}<br>Tasa de ingreso: %{y:.2f} %<extra></extra>",
    ))
    fig.update_xaxes(title="Decil de puntaje en matemáticas", dtick=1)
    fig.update_yaxes(title="Tasa de ingreso (%)", range=[0, 100], ticksuffix=" %")
    return aplicar_formato(fig, alto=330)


def _indicador(titulo, valor, detalle):
    """Crear una tarjeta de indicador con el estilo del dashboard."""
    return html.Div(className="tarjeta indicador", children=[
        html.Div(titulo, className="indicador-titulo"),
        html.Div(valor, className="indicador-valor"),
        html.Div(detalle, className="indicador-detalle"),
    ])


def _panel(titulo, figura, nota=""):
    """Crear un panel para una gráfica y su nota metodológica."""
    hijos = [html.H3(titulo), dcc.Graph(figure=figura, config={"displayModeBar": False})]
    if nota:
        hijos.append(html.P(nota, className="nota"))
    return html.Div(className="tarjeta panel", children=hijos)


def layout() -> html.Div:
    """Construir la página de brechas de acceso a educación superior."""
    brecha_internet = float(
        INTERNET.loc[INTERNET["categoria"] == "Sí", "tasa"].iloc[0]
        - INTERNET.loc[INTERNET["categoria"] == "No", "tasa"].iloc[0]
    )
    brecha_area = float(
        AREA.loc[AREA["categoria"] == "Urbano", "tasa"].iloc[0]
        - AREA.loc[AREA["categoria"] == "Rural", "tasa"].iloc[0]
    )
    brecha_computador = float(
        COMPUTADOR.loc[COMPUTADOR["categoria"] == "Sí", "tasa"].iloc[0]
        - COMPUTADOR.loc[COMPUTADOR["categoria"] == "No", "tasa"].iloc[0]
    )

    return html.Div([
        html.Div(className="encabezado", children=[
            html.H1("Brechas en el ingreso a la educación superior"),
            html.P(
                "Comparación descriptiva de las tasas de ingreso según condiciones "
                "socioeconómicas, familiares y características del colegio."
            ),
        ]),

        html.Div(className="fila-indicadores", children=[
            _indicador("Brecha por internet", f"{formato_numero(brecha_internet, 1)} p.p.",
                       "Diferencia entre estudiantes con y sin internet"),
            _indicador("Brecha rural–urbana", f"{formato_numero(brecha_area, 1)} p.p.",
                       "Diferencia entre colegios urbanos y rurales"),
            _indicador("Brecha por computador", f"{formato_numero(brecha_computador, 1)} p.p.",
                       "Diferencia entre estudiantes con y sin computador"),
        ]),

        html.Div(className="fila", children=[
            _panel("Ingreso según estrato de vivienda", _grafica_barras(ESTRATO, "categoria"),
                   "La categoría sin estrato se presenta por separado."),
            _panel("Ingreso según ubicación del colegio", _grafica_barras(AREA, "categoria")),
        ]),
        html.Div(className="fila", children=[
            _panel("Ingreso según acceso a internet", _grafica_barras(INTERNET, "categoria")),
            _panel("Ingreso según disponibilidad de computador", _grafica_barras(COMPUTADOR, "categoria")),
        ]),
        html.Div(className="fila", children=[
            _panel("Ingreso según nivel educativo de la madre",
                   _grafica_barras(EDUCACION_MADRE, "categoria", alto=360),
                   "Las categorías corresponden a los códigos registrados en el resumen de datos."),
            _panel("Ingreso según decil de matemáticas", _grafica_deciles(),
                   "La tasa corresponde al ingreso observado (enroll_full)."),
        ]),

        html.P(
            "Nota: las tasas describen asociaciones observadas en los datos y no "
            "demuestran relaciones causales. Las categorías sin información se excluyen "
            "de las comparaciones cuando no es posible asignarles una etiqueta.",
            className="nota",
        ),
    ])
