from typing import Any

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from loguru import logger

from app.api import api_router
from app.config import settings, setup_app_logging

setup_app_logging(config=settings)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

root_router = APIRouter()


@root_router.get("/")
def index(request: Request) -> Any:
    """Página de bienvenida."""
    body = (
        "<html><body style='padding: 10px; font-family: sans-serif;'>"
        "<h1>API · Riesgo de no ingreso a la educación superior</h1>"
        "<div>Documentación: <a href='/docs'>/docs</a></div>"
        "</body></html>"
    )
    return HTMLResponse(content=body)


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origen) for origen in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    logger.warning("Ejecutando en modo desarrollo.")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
