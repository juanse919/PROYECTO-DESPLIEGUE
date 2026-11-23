
# Importar los componentes necesarios de Dash
from dash import html


# Construir la página de presentación del proyecto
def layout() -> html.Div:

    return html.Div([

        html.Div(className="encabezado", children=[
            html.H1("Acerca del proyecto"),
            html.P(
                "Trayectorias estudiantiles | Saber 11 → Educación Superior. "
                "Análisis del acceso y la continuidad educativa en Colombia."
            ),
        ]),

        html.Div(className="tarjeta", children=[

            html.H3("Contexto y propósito"),
            html.P(
                "El tránsito de la educación media a la educación superior "
                "representa un desafío para muchos bachilleres en Colombia. "
                "Las trayectorias de ingreso presentan diferencias asociadas "
                "con las condiciones académicas, socioeconómicas y territoriales "
                "de los estudiantes."
            ),
            html.P(
                "Este proyecto busca analizar dichas trayectorias a partir de "
                "la información de Saber 11 y los registros de educación superior, "
                "facilitando la identificación de patrones y brechas de acceso."
            ),

            html.H3("Objetivo"),
            html.P(
                "Describir el comportamiento del ingreso a la educación superior "
                "y reconocer las diferencias entre grupos de estudiantes, "
                "considerando características individuales, familiares, "
                "institucionales y territoriales. Adicionalmente, incorporar "
                "un modelo predictivo que estime la probabilidad de no ingreso "
                "a educación superior."
            ),

            html.H3("Alcance del tablero"),
            html.P(
                "El tablero reúne información de las cohortes de estudiantes "
                "que presentaron Saber 11 entre 2012 y 2025. Permite explorar "
                "indicadores generales, evolución del ingreso por cohorte, "
                "distribución territorial y diferencias según condiciones "
                "socioeconómicas y características de los colegios."
            ),
            html.P(
                "La sección de Predicciones complementa el análisis descriptivo "
                "mediante una estimación del riesgo de no ingreso, a partir de "
                "las características ingresadas para un estudiante."
            ),

            html.H3("Fuentes de información"),
            html.P(
                "La fuente principal corresponde a una base de datos suministrada "
                "por el ICFES, con 7.138.927 registros de estudiantes que "
                "presentaron Saber 11 entre 2012 y 2025 y 89 variables. "
                "La información integra resultados de Saber 11, registros "
                "de matrícula del Sistema Nacional de Información de la "
                "Educación Superior (SNIES) y resultados de Saber Pro y Saber TyT."
            ),
            html.P(
                "Para el desarrollo del tablero se utilizan archivos resumidos "
                "y datos preparados durante el proceso de análisis."
            ),

        ]),

    ])
    