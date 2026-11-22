from pathlib import Path
from typing import List

import yaml
from pydantic import BaseModel

import modelo_ingreso

PAQUETE_RAIZ = Path(modelo_ingreso.__file__).resolve().parent
RAIZ = PAQUETE_RAIZ.parent
ARCHIVO_CONFIG = PAQUETE_RAIZ / "config.yml"
DIRECTORIO_DATOS = PAQUETE_RAIZ / "datasets"
DIRECTORIO_MODELOS = PAQUETE_RAIZ / "trained"


class ConfigModelo(BaseModel):
    nombre_paquete: str
    nombre_modelo_guardado: str
    ruta_datos: str
    fraccion_muestra: float
    tamano_bloque: int
    semilla: int
    columna_cohorte: str
    cohortes_entrenamiento: List[int]
    cohortes_validacion: List[int]
    objetivo_base: str
    objetivo: str
    variables_numericas: List[str]
    variables_categoricas: List[str]
    n_estimators: int
    max_depth: int
    learning_rate: float
    subsample: float
    colsample_bytree: float
    umbral: float
    nombre_experimento: str

    @property
    def variables(self) -> List[str]:
        return self.variables_numericas + self.variables_categoricas


def cargar_config(ruta: Path = ARCHIVO_CONFIG) -> ConfigModelo:
    with open(ruta, encoding="utf-8") as archivo:
        return ConfigModelo(**yaml.safe_load(archivo))


config = cargar_config()
