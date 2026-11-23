
# Importar las librerías necesarias
from dash import html, dcc
from api_cliente import OPCIONES, NUMERICAS, predecir


# Crear los campos numéricos del formulario
def crear_campos_numericos():

    campos = []

    for variable, rango in NUMERICAS.items():

        minimo, maximo = rango

        campo = html.Div([
            html.Label(variable.replace("_", " ").capitalize()),
            dcc.Input(
                id=f"pred-{variable}",
                type="number",
                min=minimo,
                max=maximo,
                step=1,
                placeholder=f"{minimo} a {maximo}",
                style={"width": "100%"}
            )
        ], style={
            "flex": "1",
            "minWidth": "220px",
            "marginBottom": "15px"
        })

        campos.append(campo)

    return campos


# Crear los campos categóricos del formulario
def crear_campos_categoricos():

    campos = []

    for variable, opciones in OPCIONES.items():

        opciones_dropdown = []

        for etiqueta, valor in opciones.items():
            opciones_dropdown.append({
                "label": etiqueta,
                "value": valor
            })

        campo = html.Div([
            html.Label(variable.replace("_", " ").capitalize()),
            dcc.Dropdown(
                id=f"pred-{variable}",
                options=opciones_dropdown,
                placeholder="Seleccionar...",
                clearable=True
            )
        ], style={
            "flex": "1",
            "minWidth": "220px",
            "marginBottom": "15px"
        })

        campos.append(campo)

    return campos


# Construir la página de predicciones
def layout():

    return html.Div([

        html.H1("Predicciones de riesgo de no ingreso"),

        html.P(
            "Ingrese la información del estudiante para estimar "
            "la probabilidad de no ingresar a educación superior "
            "durante los cinco años posteriores a Saber 11."
        ),

        html.Div([

            html.H2("Información del estudiante"),

            html.H3("Variables numéricas"),

            html.Div(
                crear_campos_numericos(),
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "gap": "15px"
                }
            ),

            html.H3("Variables categóricas"),

            html.Div(
                crear_campos_categoricos(),
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "gap": "15px"
                }
            ),

            html.Button(
                "Calcular predicción",
                id="btn-predecir",
                n_clicks=0,
                style={
                    "padding": "12px 22px",
                    "backgroundColor": "#1F5F7A",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "6px",
                    "fontSize": "16px",
                    "fontWeight": "bold",
                    "cursor": "pointer",
                    "marginTop": "10px"
                }
            )

        ], style={
            "backgroundColor": "white",
            "padding": "20px",
            "borderRadius": "10px",
            "marginTop": "20px"
        }),

        # Mostrar el indicador mientras se calcula la predicción
        dcc.Loading(
            id="cargando-prediccion",
            type="circle",
            color="#1F5F7A",
            children=html.Div(
                id="resultado-prediccion",
                style={
                    "marginTop": "20px",
                    "scrollMarginTop": "30px"
                }
            )
        ),

        # Registrar el estado del desplazamiento automático
        dcc.Store(id="estado-desplazamiento")

    ], style={
        "maxWidth": "1200px",
        "margin": "0 auto"
    })


# Generar la predicción mediante la API del modelo
def generar_prediccion(n_clicks, *valores):

    # Validar que se hayan ingresado datos
    if not any(valor is not None for valor in valores):
        return html.Div(
            "Ingrese al menos una variable para calcular la predicción.",
            style={
                "color": "#B45309",
                "backgroundColor": "#FEF3C7",
                "padding": "15px",
                "borderRadius": "8px"
            }
        )

    # Organizar los datos del estudiante
    variables = list(NUMERICAS.keys()) + list(OPCIONES.keys())

    estudiante = {}

    for variable, valor in zip(variables, valores):
        if valor is not None:
            estudiante[variable] = valor

    # Consultar el modelo mediante la API
    resultado = predecir(estudiante)

    # Verificar si ocurrió un error en la conexión
    if "error" in resultado:
        return html.Div([
            html.H3("No fue posible generar la predicción"),
            html.P(resultado["error"]),
            html.P(
                "Verifique que la API esté ejecutándose en el puerto 8001."
            )
        ], style={
            "color": "#B91C1C",
            "backgroundColor": "#FEE2E2",
            "padding": "20px",
            "borderRadius": "10px",
            "marginTop": "20px"
        })

    # Obtener los resultados del modelo
    probabilidad = resultado["probabilidad"]
    alerta = resultado["alerta"]
    umbral = resultado["umbral"]
    version = resultado["version"]

    porcentaje = f"{probabilidad:.1%}"

    # Clasificar el nivel de riesgo
    if alerta == 1:
        riesgo = "Riesgo alto"
        color = "#B91C1C"
    else:
        riesgo = "Riesgo no alto"
        color = "#18794E"

    # Mostrar los resultados de la predicción
    return html.Div([

        html.H2(
            "Resultado de la predicción",
            style={
                "color": "#173F52",
                "marginBottom": "25px"
            }
        ),

        html.Div([
            html.Div([
                html.P(
                    "Probabilidad de no ingreso",
                    style={"fontSize": "18px"}
                ),
                html.H1(
                    porcentaje,
                    style={
                        "color": "#1F5F7A",
                        "fontSize": "42px",
                        "marginBottom": "10px"
                    }
                )
            ], style={
                "backgroundColor": "#EAF2F8",
                "padding": "25px",
                "borderRadius": "10px",
                "flex": "1"
            }),

            html.Div([
                html.P(
                    "Clasificación del riesgo",
                    style={"fontSize": "18px"}
                ),
                html.H2(
                    riesgo,
                    style={
                        "color": color,
                        "fontSize": "30px"
                    }
                )
            ], style={
                "backgroundColor": "#EAF2F8",
                "padding": "25px",
                "borderRadius": "10px",
                "flex": "1"
            })

        ], style={
            "display": "flex",
            "gap": "15px",
            "flexWrap": "wrap"
        }),

        html.P(
            f"Umbral del modelo: {umbral:.2f}",
            style={"marginTop": "25px"}
        ),

        html.P(f"Versión del modelo: {version}")

    ], style={
        "backgroundColor": "white",
        "padding": "25px",
        "borderRadius": "12px",
        "marginTop": "20px",
        "marginBottom": "30px",
        "border": "2px solid #D5E5EF",
        "boxShadow": "0 3px 10px rgba(0,0,0,0.06)"
    })
