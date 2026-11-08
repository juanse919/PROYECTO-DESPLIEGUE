"""Página Resumen: indicadores generales del tránsito de Saber 11 a la educación superior."""

import json
import re
from urllib.request import urlopen

import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

import datos
from estilo import (AMARILLO, AZUL, AZUL_OSCURO, GRIS, TURQUESA, TURQUESA_CLARO,
                    aplicar_formato, formato_numero)

COHORTES = datos.cargar_cohortes()
ESTRATO = datos.cargar_estrato()
DEPARTAMENTOS = datos.cargar_departamentos()
HORIZONTE = datos.cargar_horizonte()

ANIO_MIN = int(COHORTES["año"].min())
ANIO_MAX = int(COHORTES["año"].max())
ULTIMA = datos.ULTIMA_COHORTE_COMPLETA


# ---------- Componentes ----------

def tarjeta(titulo: str, id_valor: str, id_detalle: str) -> html.Div:
    return html.Div(
        className="tarjeta indicador",
        children=[
            html.Div(titulo, className="indicador-titulo"),
            html.Div(id=id_valor, className="indicador-valor"),
            html.Div(id=id_detalle, className="indicador-detalle"),
        ],
    )


def panel(titulo: str, contenido, nota: str = "", clase: str = "") -> html.Div:
    hijos = [html.H3(titulo), contenido]
    if nota:
        hijos.append(html.P(nota, className="nota"))
    return html.Div(className=f"tarjeta panel {clase}", children=hijos)


# ---------- Gráficas fijas (todas las cohortes) ----------

def grafica_estrato() -> go.Figure:
    fig = go.Figure(go.Bar(
        x=ESTRATO["tasa"], y=ESTRATO["categoria"], orientation="h",
        marker_color=[GRIS if c == "Sin estrato" else TURQUESA for c in ESTRATO["categoria"]],
        text=[f"{formato_numero(t, 1)} %" for t in ESTRATO["tasa"]], textposition="outside",
        customdata=ESTRATO["estudiantes"],
        hovertemplate="%{y}<br>Tasa de ingreso: %{x:.1f} %<br>Estudiantes: %{customdata:,}<extra></extra>",
    ))
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(range=[0, 100], ticksuffix=" %")
    return aplicar_formato(fig, alto=300)


def grafica_departamentos() -> go.Figure:
    """Mapa coroplético de la tasa de ingreso por departamento del colegio."""
    url_geojson = (
        "https://raw.githubusercontent.com/ytolosa/mapas-colombia/"
        "main/output/geojson/col_departamentos_inset_nacional.geojson"
    )
    fig = go.Figure()

    try:
        with urlopen(url_geojson, timeout=15) as respuesta:
            geojson = json.load(respuesta)

        def normalizar_codigo(valor):
            return re.sub(r"\D", "", str(valor)).lstrip("0")

        caracteristicas = geojson.get("features", [])
        if not caracteristicas:
            raise ValueError("El archivo geográfico no contiene departamentos.")

        codigos_datos = DEPARTAMENTOS["categoria"].astype(int).astype(str).tolist()
        propiedades = caracteristicas[0].get("properties", {})
        clave_codigo = None
        mejor_coincidencia = 0

        for clave in propiedades:
            codigos_mapa = {
                normalizar_codigo(feature.get("properties", {}).get(clave))
                for feature in caracteristicas
            }
            coincidencias = sum(
                normalizar_codigo(codigo) in codigos_mapa for codigo in codigos_datos
            )
            if coincidencias > mejor_coincidencia:
                mejor_coincidencia = coincidencias
                clave_codigo = clave

        if clave_codigo is None or mejor_coincidencia < 20:
            raise ValueError("No se pudieron relacionar los códigos DANE con el mapa.")

        codigos_mapa = {
            normalizar_codigo(feature["properties"][clave_codigo]):
            feature["properties"][clave_codigo]
            for feature in caracteristicas
            if clave_codigo in feature.get("properties", {})
        }
        departamentos_validos = DEPARTAMENTOS[
            DEPARTAMENTOS["categoria"].astype(int).astype(str).map(
                lambda codigo: normalizar_codigo(codigo) in codigos_mapa
            )
        ].copy()
        departamentos_validos["codigo_mapa"] = departamentos_validos[
            "categoria"
        ].astype(int).astype(str).map(
            lambda codigo: codigos_mapa[normalizar_codigo(codigo)]
        )

        fig.add_trace(go.Choropleth(
            geojson=geojson,
            featureidkey=f"properties.{clave_codigo}",
            locations=departamentos_validos["codigo_mapa"],
            z=departamentos_validos["tasa"],
            customdata=departamentos_validos[["departamento", "estudiantes"]].to_numpy(),
            colorscale=[[0, TURQUESA_CLARO], [0.5, TURQUESA], [1, AZUL_OSCURO]],
            zmin=30,
            zmax=75,
            marker_line_color="white",
            marker_line_width=0.8,
            colorbar=dict(title="Tasa de ingreso", ticksuffix=" %"),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Tasa de ingreso: %{z:.2f} %<br>"
                "Estudiantes: %{customdata[1]:,}<extra></extra>"
            ),
        ))
        fig.update_geos(
            fitbounds="locations", visible=False, showcountries=False,
            showcoastlines=False, bgcolor="rgba(0,0,0,0)",
        )
        fig.update_layout(
            height=640, margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Segoe UI, Inter, Helvetica, Arial, sans-serif", color=AZUL_OSCURO),
        )
    except Exception as error:
        fig.add_annotation(
            text=("No fue posible cargar el mapa geográfico. "
                  "Verifica la conexión a internet y vuelve a cargar la página."),
            x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False,
            font=dict(color=GRIS, size=13),
        )
        fig.update_layout(height=640, margin=dict(l=10, r=10, t=10, b=10))

    return fig


def grafica_horizonte() -> go.Figure:
    colores = [AZUL_OSCURO, AZUL, TURQUESA, TURQUESA_CLARO, "#C9D3D8"]
    fig = go.Figure(go.Bar(
        x=HORIZONTE["pct"], y=HORIZONTE["horizonte"], orientation="h", marker_color=colores,
        text=[f"{formato_numero(p, 1)} %" for p in HORIZONTE["pct"]], textposition="outside",
        customdata=HORIZONTE["estudiantes"],
        hovertemplate="%{y}<br>%{x:.1f} % de los estudiantes<br>%{customdata:,} estudiantes<extra></extra>",
    ))
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(range=[0, 55], ticksuffix=" %")
    return aplicar_formato(fig, alto=260)


# ---------- Layout ----------

def layout() -> html.Div:
    return html.Div([
        html.Div(className="encabezado", children=[
            html.H1("Trayectorias estudiantiles | Saber 11 → Educación Superior"),
            html.P("Seguimiento del tránsito desde la presentación de Saber 11 hasta el ingreso "
                   "a la educación superior. Base: 7.138.927 estudiantes, cohortes 2012–2025."),
        ]),

        html.Div(className="tarjeta filtro", children=[
            html.Div("Cohorte Saber 11", className="filtro-titulo"),
            dcc.RangeSlider(
                id="resumen-cohortes", min=ANIO_MIN, max=ANIO_MAX, step=1,
                value=[ANIO_MIN, ULTIMA],
                marks={a: str(a) for a in range(ANIO_MIN, ANIO_MAX + 1)},
            ),
            html.Div(id="resumen-aviso", className="aviso"),
        ]),

        html.Div(className="fila-indicadores", children=[
            tarjeta("Estudiantes analizados", "kpi-estudiantes", "kpi-estudiantes-det"),
            tarjeta("Tasa de ingreso", "kpi-observada", "kpi-observada-det"),
            tarjeta("Ingreso en 5 años", "kpi-cinco", "kpi-cinco-det"),
            tarjeta("No ingreso en 5 años", "kpi-riesgo", "kpi-riesgo-det"),
        ]),

        html.Div(className="fila", children=[
            panel("Evolución del ingreso por cohorte",
                  dcc.Graph(id="resumen-evolucion", config={"displayModeBar": False}),
                  "Las cohortes 2021–2025 (zona sombreada) aún no completan cinco años de "
                  "seguimiento, por lo que sus tasas están subestimadas.",
                  clase="ancho-2"),
            panel("Ingreso según estrato",
                  dcc.Graph(figure=grafica_estrato(), config={"displayModeBar": False}),
                  "Ingreso observado, todas las cohortes."),
        ]),

        html.Div(className="fila", children=[
            panel("Ingreso por departamento del colegio",
                  dcc.Graph(figure=grafica_departamentos(), config={"displayModeBar": False}),
                  "Tasa de ingreso observado según el departamento de ubicación del colegio. "
                  "Pasa el cursor sobre cada departamento para consultar la tasa y los estudiantes."),
            panel("¿Cuándo ingresan los bachilleres?",
                  dcc.Graph(figure=grafica_horizonte(), config={"displayModeBar": False}),
                  "Momento del primer ingreso respecto al año de Saber 11, todas las cohortes. "
                  "El modelo predictivo estima el riesgo de no ingresar en los primeros cinco años."),
        ]),
    ])



# ---------- Callbacks ----------

@callback(
    Output("kpi-estudiantes", "children"), Output("kpi-estudiantes-det", "children"),
    Output("kpi-observada", "children"), Output("kpi-observada-det", "children"),
    Output("kpi-cinco", "children"), Output("kpi-cinco-det", "children"),
    Output("kpi-riesgo", "children"), Output("kpi-riesgo-det", "children"),
    Output("resumen-aviso", "children"),
    Output("resumen-evolucion", "figure"),
    Input("resumen-cohortes", "value"),
)
def actualizar_resumen(rango):
    desde, hasta = rango
    r = datos.resumen_cohortes(COHORTES, desde, hasta)
    periodo = f"Cohortes {desde}–{hasta}" if desde != hasta else f"Cohorte {desde}"
    aviso = ("Atención: el rango incluye cohortes posteriores a 2020, que aún no completan "
             "cinco años de seguimiento." if r["incluye_incompletas"] else "")
    return (
        formato_numero(r["estudiantes"]), periodo,
        f"{formato_numero(r['tasa_observada'], 1)} %", "Ingreso observado en cualquier momento",
        f"{formato_numero(r['tasa_5anios'], 1)} %", "Ingreso hasta 5 años después de Saber 11",
        f"{formato_numero(r['tasa_no_ingreso_5anios'], 1)} %",
        f"{formato_numero(r['no_ingreso_5anios'])} estudiantes (variable objetivo del modelo)",
        aviso,
        grafica_evolucion(desde, hasta),
    )


def grafica_evolucion(desde: int, hasta: int) -> go.Figure:
    sel = COHORTES[COHORTES["año"].between(desde, hasta)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sel["año"], y=sel["tasa"], name="Ingreso observado (cualquier momento)",
        mode="lines+markers", line=dict(color=AMARILLO, width=3),
        hovertemplate="Cohorte %{x}<br>Ingreso observado: %{y:.1f} %<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=sel["año"], y=sel["tasa_5anios"], name="Ingreso en 5 años",
        mode="lines+markers", line=dict(color=AZUL, width=3),
        hovertemplate="Cohorte %{x}<br>Ingreso en 5 años: %{y:.1f} %<extra></extra>",
    ))
    if hasta > ULTIMA:
        fig.add_vrect(x0=max(desde, ULTIMA + 1) - 0.5, x1=hasta + 0.5, fillcolor=GRIS,
                      opacity=0.12, line_width=0,
                      annotation_text="Seguimiento incompleto", annotation_position="top left")
    fig.update_yaxes(range=[0, 80], ticksuffix=" %")
    fig.update_xaxes(dtick=1)
    return aplicar_formato(fig, alto=320)
