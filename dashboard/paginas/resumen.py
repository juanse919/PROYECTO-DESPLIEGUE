"""Página Resumen: indicadores generales del tránsito de Saber 11 a la educación superior."""

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
    fig = go.Figure(go.Bar(
        x=DEPARTAMENTOS["tasa"], y=DEPARTAMENTOS["departamento"], orientation="h",
        marker=dict(color=DEPARTAMENTOS["tasa"], colorscale=[[0, TURQUESA_CLARO], [1, AZUL_OSCURO]]),
        customdata=DEPARTAMENTOS["estudiantes"],
        hovertemplate="%{y}<br>Tasa de ingreso: %{x:.1f} %<br>Estudiantes: %{customdata:,}<extra></extra>",
    ))
    promedio = 100 * DEPARTAMENTOS["ingresaron"].sum() / DEPARTAMENTOS["estudiantes"].sum()
    fig.add_vline(x=promedio, line_dash="dash", line_color=AMARILLO,
                  annotation_text=f"Nacional {formato_numero(promedio, 1)} %",
                  annotation_position="top")
    fig.update_xaxes(range=[0, 80], ticksuffix=" %")
    fig.update_yaxes(tickfont=dict(size=11))
    return aplicar_formato(fig, alto=640)


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
                  "Ingreso observado, todas las cohortes. La línea amarilla marca el promedio nacional."),
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
