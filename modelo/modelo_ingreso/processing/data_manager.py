import os
from pathlib import Path
from typing import Tuple

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from modelo_ingreso import __version__
from modelo_ingreso.config.core import DIRECTORIO_MODELOS, RAIZ, config


def ruta_datos() -> Path:
    """Ruta de la base: variable de entorno RUTA_DATOS o la definida en config.yml."""
    ruta = Path(os.getenv("RUTA_DATOS", config.ruta_datos))
    return ruta if ruta.is_absolute() else (RAIZ / ruta).resolve()


def cargar_datos_modelado() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Lee la base .dta por bloques, toma la muestra reproducible y separa por cohortes."""
    import pyreadstat  # solo se necesita para entrenar

    inicio_ent, fin_ent = config.cohortes_entrenamiento
    inicio_val, fin_val = config.cohortes_validacion
    columnas = [config.columna_cohorte, config.objetivo_base] + config.variables

    muestras = []
    lector = pyreadstat.read_file_in_chunks(
        pyreadstat.read_dta, str(ruta_datos()),
        chunksize=config.tamano_bloque, usecols=columnas,
    )
    for bloque, _ in lector:
        bloque = bloque[bloque[config.columna_cohorte].between(inicio_ent, fin_val)]
        if bloque.empty:
            continue
        muestras.append(bloque.sample(frac=config.fraccion_muestra, random_state=config.semilla))

    datos = pd.concat(muestras, ignore_index=True)
    datos[config.objetivo] = (1 - datos[config.objetivo_base]).astype(int)

    cohorte = datos[config.columna_cohorte]
    entrenamiento = datos[cohorte.between(inicio_ent, fin_ent)].copy()
    validacion = datos[cohorte.between(inicio_val, fin_val)].copy()
    return entrenamiento, validacion


def nombre_archivo_modelo() -> str:
    return f"{config.nombre_modelo_guardado}{__version__}.pkl"


def guardar_pipeline(pipeline: Pipeline) -> Path:
    """Guarda el modelo entrenado y borra las versiones anteriores."""
    destino = DIRECTORIO_MODELOS / nombre_archivo_modelo()
    for archivo in DIRECTORIO_MODELOS.glob("*.pkl"):
        archivo.unlink()
    joblib.dump(pipeline, destino)
    return destino


def cargar_pipeline() -> Pipeline:
    return joblib.load(DIRECTORIO_MODELOS / nombre_archivo_modelo())
