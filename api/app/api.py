import json
from typing import Any

import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger
from modelo_ingreso import __version__ as model_version
from modelo_ingreso.predict import make_prediction

from app import __version__, schemas
from app.config import settings

api_router = APIRouter()


@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """Estado de la API y versiones de la API y del modelo."""
    health = schemas.Health(name=settings.PROJECT_NAME, api_version=__version__,
                            model_version=model_version)
    return health.model_dump()


@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: schemas.MultipleDataInputs) -> Any:
    """Probabilidad de no ingresar a la educación superior en 5 años y alerta según el umbral."""
    datos = pd.DataFrame(jsonable_encoder(input_data.inputs))
    logger.info(f"Prediciendo {len(datos)} registro(s)")
    resultados = make_prediction(input_data=datos)

    if resultados["errors"] is not None:
        logger.warning(f"Error de validación: {resultados.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(resultados["errors"]))

    logger.info(f"Probabilidades: {resultados.get('probabilidades')}")
    return resultados
