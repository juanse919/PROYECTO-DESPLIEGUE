import math

from modelo_ingreso import __version__
from modelo_ingreso.config.core import config
from modelo_ingreso.predict import make_prediction


def test_make_prediction(estudiantes):
    resultado = make_prediction(input_data=estudiantes)

    assert resultado["errors"] is None
    assert resultado["version"] == __version__
    assert resultado["umbral"] == config.umbral

    probabilidades = resultado["probabilidades"]
    assert len(probabilidades) == len(estudiantes)
    assert all(0 <= p <= 1 and not math.isnan(p) for p in probabilidades)
    assert resultado["alertas"] == [int(p >= config.umbral) for p in probabilidades]

    # El perfil con condiciones de riesgo debe tener mayor probabilidad de no ingreso
    assert probabilidades[1] > probabilidades[0]


def test_variables_faltantes_y_codigos_decimales(estudiantes):
    """La API puede recibir registros incompletos o códigos como 1.0 en vez de 1."""
    datos = estudiantes.drop(columns=["punt_ingles", "fami_cuartoshogar"])
    datos["fami_estratovivienda"] = datos["fami_estratovivienda"].astype(float)
    resultado = make_prediction(input_data=datos)
    assert resultado["errors"] is None
    assert len(resultado["probabilidades"]) == 2


def test_entrada_invalida(estudiantes):
    datos = estudiantes.copy()
    datos["punt_matematicas"] = ["sesenta", "x"]
    resultado = make_prediction(input_data=datos)
    assert resultado["errors"] is not None
    assert resultado["probabilidades"] is None
