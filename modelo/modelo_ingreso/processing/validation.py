from typing import List, Optional, Tuple, Union

import pandas as pd
from pydantic import BaseModel, ValidationError

from modelo_ingreso.config.core import config

Valor = Optional[Union[int, float, str]]


class EstudianteEntrada(BaseModel):
    """Información disponible al presentar Saber 11 (códigos como en la base ICFES)."""
    estu_edad: Optional[float] = None
    punt_matematicas: Optional[float] = None
    punt_ingles: Optional[float] = None
    punt_lectura_critica: Optional[float] = None
    punt_c_naturales: Optional[float] = None
    fami_cuartoshogar: Optional[float] = None
    fami_personashogar: Optional[float] = None
    estu_genero: Valor = None            # 0 = Masculino, 1 = Femenino
    cole_genero: Valor = None            # FEMENINO, MASCULINO, MIXTO
    cole_calendario: Valor = None        # A, B, OTRO
    cole_area_ubicacion: Valor = None    # URBANO, RURAL
    cole_jornada: Valor = None           # COMPLETA, MAÑANA, NOCHE, SABATINA, TARDE, UNICA
    cole_cod_depto_ubicacion: Valor = None  # código DANE del departamento (11 = Bogotá)
    estu_tieneetnia: Valor = None        # Si, No
    fami_educacionmadre: Valor = None    # 0 Ninguna … 4 Profesional o superior
    fami_estratovivienda: Valor = None   # 0 (sin estrato) a 6
    fami_tienecomputador: Valor = None   # 0 = No, 1 = Sí
    fami_tieneinternet: Valor = None     # 0 = No, 1 = Sí
    cole_naturaleza: Valor = None        # 0 = No oficial, 1 = Oficial


class EntradasMultiples(BaseModel):
    inputs: List[EstudianteEntrada]


def validar_entradas(datos: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[str]]:
    """Revisa los registros contra el esquema y completa las columnas que falten."""
    datos = datos.copy()
    for columna in config.variables:
        if columna not in datos:
            datos[columna] = None
    datos = datos[config.variables]
    errores = None
    try:
        registros = datos.astype(object).where(pd.notna(datos), None).to_dict(orient="records")
        EntradasMultiples(inputs=registros)
    except ValidationError as error:
        errores = error.json()
    return datos, errores
