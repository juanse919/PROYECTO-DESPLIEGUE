from typing import Union

import pandas as pd

from modelo_ingreso import __version__
from modelo_ingreso.config.core import config
from modelo_ingreso.processing.data_manager import cargar_pipeline
from modelo_ingreso.processing.validation import validar_entradas

_pipeline = None


def _modelo():
    global _pipeline
    if _pipeline is None:
        _pipeline = cargar_pipeline()
    return _pipeline


def make_prediction(*, input_data: Union[pd.DataFrame, dict], umbral: float = None) -> dict:
    """Probabilidad de no ingresar a la educación superior en 5 años y alerta según el umbral."""
    datos = pd.DataFrame(input_data)
    umbral = config.umbral if umbral is None else umbral
    validados, errores = validar_entradas(datos)
    resultado = {"probabilidades": None, "alertas": None, "umbral": umbral,
                 "version": __version__, "errors": errores}
    if not errores:
        probabilidades = _modelo().predict_proba(validados)[:, 1]
        resultado["probabilidades"] = [round(float(p), 4) for p in probabilidades]
        resultado["alertas"] = [int(p >= umbral) for p in probabilidades]
    return resultado
