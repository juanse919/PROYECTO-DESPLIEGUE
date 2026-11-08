"""Página Acerca del proyecto."""

from dash import html


def layout() -> html.Div:
    """Presentar el contexto, propósito, alcance y fuentes del proyecto."""
    return html.Div([
        html.Div(className="encabezado", children=[
            html.H1("Acerca del proyecto"),
            html.P(
                "Trayectorias estudiantiles | Saber 11 → Educación Superior. "
                "Una mirada descriptiva al tránsito de los bachilleres hacia "
                "la educación superior en Colombia."
            ),
        ]),

        html.Div(className="tarjeta", children=[
            html.H3("Contexto del problema"),
            html.P(
                "El paso de la educación media a la educación superior continúa "
                "siendo un desafío en Colombia. Aunque una parte de los bachilleres "
                "inicia estudios superiores después de presentar Saber 11, otros "
                "no registran ingreso o lo hacen varios años más tarde. Estas "
                "trayectorias pueden presentar diferencias relacionadas con las "
                "condiciones académicas, socioeconómicas y territoriales de los "
                "estudiantes."
            ),
            html.P(
                "Comprender cómo se comporta este tránsito permite reconocer "
                "diferencias entre grupos de estudiantes y territorios, así como "
                "aportar información para la reflexión sobre las oportunidades "
                "de continuidad educativa. El proyecto se enmarca en el interés "
                "por comprender el acceso a la educación superior y ofrecer "
                "información descriptiva que facilite su análisis."
            ),

            html.H3("Propósito del proyecto"),
            html.P(
                "Analizar las trayectorias de los estudiantes desde la presentación "
                "de Saber 11 hasta su posible ingreso a la educación superior "
                "formal en Colombia. El tablero busca organizar y presentar "
                "indicadores que permitan conocer cuántos estudiantes registran "
                "ingreso, en qué momento ocurre y cómo varían las tasas según "
                "características del estudiante, su entorno familiar, el colegio "
                "y el territorio."
            ),
            html.P(
                "Con esta información se busca facilitar la identificación de "
                "diferencias de acceso y aportar elementos para comprender dónde "
                "se presentan mayores desafíos de continuidad educativa. Los "
                "resultados constituyen un insumo descriptivo para el análisis "
                "del problema y no una valoración individual de los estudiantes."
            ),

            html.H3("Pregunta orientadora"),
            html.P(
                "¿Cómo se comporta el ingreso a la educación superior de los "
                "estudiantes que presentaron Saber 11 en Colombia y qué diferencias "
                "se observan según sus condiciones académicas, socioeconómicas "
                "y territoriales?"
            ),

            html.H3("Alcance del tablero"),
            html.P(
                "El tablero presenta información agregada de las cohortes de "
                "estudiantes que presentaron Saber 11 entre 2012 y 2025. Permite "
                "consultar indicadores generales, observar la evolución del "
                "ingreso por cohorte y comparar las tasas de ingreso según "
                "estrato socioeconómico, departamento y otras características "
                "disponibles en los datos."
            ),
            html.P(
                "La consulta se organiza en las secciones Resumen y Brechas, "
                "además de esta página informativa. La página Resumen reúne "
                "indicadores generales, evolución por cohorte, ingreso por "
                "estrato, distribución territorial y momento del primer ingreso. "
                "La página Brechas compara las tasas según condiciones del hogar, "
                "del estudiante y del colegio, como ubicación, acceso a internet "
                "y disponibilidad de computador."
            ),
            html.P(
                "Para facilitar la consulta y mejorar el desempeño de la "
                "aplicación, el tablero utiliza archivos de datos resumidos "
                "generados durante la exploración, en lugar de cargar directamente "
                "la base completa en cada consulta."
            ),

            html.H3("Fuentes y datos"),
            html.P(
                "La fuente principal corresponde a una base de datos suministrada "
                "por el ICFES, con 7.138.927 registros de estudiantes que "
                "presentaron Saber 11 entre 2012 y 2025 y 89 variables. Según la "
                "documentación del proyecto, la base integra información de los "
                "resultados de Saber 11, registros de matrícula del Sistema "
                "Nacional de Información de la Educación Superior (SNIES) y "
                "resultados de Saber Pro y Saber TyT."
            ),
            html.P(
                "La información permite relacionar los resultados de la prueba "
                "Saber 11 con los registros disponibles de ingreso a la educación "
                "superior formal. Para el tablero se emplean resúmenes y archivos "
                "CSV derivados del proceso de exploración y preparación de los "
                "datos."
            ),

            html.H3("Metodología de consulta"),
            html.P(
                "El análisis parte de la revisión y exploración de la información "
                "disponible. A partir de ella se construyen resúmenes por cohorte "
                "y por diferentes características de los estudiantes. Las tasas "
                "de ingreso representan la proporción de estudiantes de cada "
                "grupo que cuenta con un registro de ingreso a educación superior "
                "en la información analizada."
            ),
            html.P(
                "También se distingue entre el ingreso observado en cualquier "
                "momento registrado y el ingreso dentro de los cinco años "
                "posteriores a la presentación de Saber 11. Esta distinción es "
                "importante porque no todas las cohortes cuentan con el mismo "
                "tiempo de seguimiento. Por ello, las cohortes recientes deben "
                "interpretarse con precaución cuando aún no completan la ventana "
                "de observación de cinco años."
            ),

            html.H3("Consideraciones y limitaciones"),
            html.P(
                "Los registros del SNIES permiten identificar matrículas en "
                "educación superior formal en Colombia, pero no incluyen estudios "
                "realizados en el exterior ni programas de educación para el "
                "trabajo. En consecuencia, algunos estudiantes pueden no tener "
                "un registro de ingreso en la fuente analizada aunque continúen "
                "su formación por otras vías."
            ),
            html.P(
                "Además, la disponibilidad y completitud de algunas variables "
                "pueden variar entre cohortes. Las comparaciones deben considerar "
                "estas diferencias y el periodo de seguimiento disponible para "
                "cada grupo."
            ),
            html.P(
                "Las tasas y brechas presentadas son descriptivas: muestran "
                "diferencias observadas entre grupos, pero no permiten afirmar "
                "por sí solas que una característica cause un mayor o menor "
                "ingreso. Los resultados dependen de la cobertura, calidad y "
                "alcance de las fuentes utilizadas."
            ),

            html.H3("Cómo interpretar los resultados"),
            html.P(
                "Los indicadores resumen el comportamiento de grupos de "
                "estudiantes y no deben utilizarse para sacar conclusiones "
                "individuales. Al comparar categorías, es importante revisar "
                "tanto la tasa como el número de estudiantes que la componen. "
                "En las gráficas interactivas, al pasar el cursor se puede "
                "consultar información adicional sobre cada grupo."
            ),
        ]),
    ])
