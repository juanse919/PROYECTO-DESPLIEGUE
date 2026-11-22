import logging
import os
import sys
from typing import List

from loguru import logger
from pydantic import BaseModel


class Settings(BaseModel):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "API riesgo de no ingreso a la educación superior"
    # Orígenes permitidos para llamar la API desde un navegador (el tablero llama desde el servidor)
    BACKEND_CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    LOGGING_LEVEL: int = logging.INFO


settings = Settings()


def setup_app_logging(config: Settings) -> None:
    logger.remove()
    logger.add(sys.stderr, level=config.LOGGING_LEVEL)
