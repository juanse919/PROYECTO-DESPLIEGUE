from typing import Any, List, Optional

from modelo_ingreso.processing.validation import EstudianteEntrada
from pydantic import BaseModel, ConfigDict


class PredictionResults(BaseModel):
    errors: Optional[Any] = None
    version: str
    umbral: float
    probabilidades: Optional[List[float]] = None
    alertas: Optional[List[int]] = None


class MultipleDataInputs(BaseModel):
    inputs: List[EstudianteEntrada]

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "inputs": [{
                "estu_edad": 17, "punt_matematicas": 62, "punt_ingles": 58,
                "punt_lectura_critica": 60, "punt_c_naturales": 55,
                "fami_cuartoshogar": 3, "fami_personashogar": 4,
                "estu_genero": 1, "cole_genero": "MIXTO", "cole_calendario": "A",
                "cole_area_ubicacion": "URBANO", "cole_jornada": "MAÑANA",
                "cole_cod_depto_ubicacion": 11, "estu_tieneetnia": "No",
                "fami_educacionmadre": 4, "fami_estratovivienda": 3,
                "fami_tienecomputador": 1, "fami_tieneinternet": 1, "cole_naturaleza": 0,
            }]
        }
    })
