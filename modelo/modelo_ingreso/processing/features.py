"""Limpieza de variables, igual para el entrenamiento y para las predicciones de la API."""
from typing import List

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


def _codigo_a_texto(valor):
    """Convierte códigos numéricos (1.0, 1, '1') en el texto '1'; deja igual las etiquetas."""
    if pd.isna(valor):
        return "Sin dato"
    texto = str(valor).strip()
    if texto == "":
        return "Sin dato"
    try:
        numero = float(texto)
        if numero.is_integer():
            return str(int(numero))
    except ValueError:
        pass
    return texto


class LimpiezaVariables(BaseEstimator, TransformerMixin):
    """Normaliza los tipos de las variables antes del preprocesamiento.

    - Numéricas: a número; los valores no válidos quedan como faltantes.
    - Categóricas: a texto, sin espacios, con 'Sin dato' para vacíos.
    - Estrato 0 se trata como la categoría 'Sin estrato'.
    - 'S' y 'Si' en estu_tieneetnia se unifican.
    """

    def __init__(self, variables_numericas: List[str], variables_categoricas: List[str]):
        self.variables_numericas = variables_numericas
        self.variables_categoricas = variables_categoricas

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        for columna in self.variables_numericas:
            X[columna] = pd.to_numeric(X[columna], errors="coerce").astype(float)
        for columna in self.variables_categoricas:
            X[columna] = X[columna].astype(object).map(_codigo_a_texto).astype(str)
        if "fami_estratovivienda" in X:
            X["fami_estratovivienda"] = X["fami_estratovivienda"].replace({"0": "Sin estrato"})
        if "estu_tieneetnia" in X:
            X["estu_tieneetnia"] = X["estu_tieneetnia"].replace({"S": "Si"})
        return X
