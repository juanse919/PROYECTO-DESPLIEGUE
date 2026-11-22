"""Conexión del tablero con la API del modelo de riesgo de no ingreso.

Uso desde una página del tablero:

    from api_cliente import OPCIONES, predecir
    resultado = predecir({"punt_matematicas": 55, "fami_estratovivienda": 2, ...})
    resultado["probabilidad"]  # 0.0 a 1.0
    resultado["alerta"]        # 1 = riesgo alto según el umbral del modelo

La URL de la API se toma de la variable de entorno API_URL (por defecto http://localhost:8001).
"""
import os

import requests

API_URL = os.getenv("API_URL", "http://localhost:8001").rstrip("/")
RUTA_PREDICCION = f"{API_URL}/api/v1/predict"
RUTA_SALUD = f"{API_URL}/api/v1/health"

# Opciones para los controles del formulario: {etiqueta visible: valor que espera la API}
OPCIONES = {
    "estu_genero": {"Masculino": 0, "Femenino": 1},
    "cole_genero": {"Mixto": "MIXTO", "Femenino": "FEMENINO", "Masculino": "MASCULINO"},
    "cole_calendario": {"A": "A", "B": "B", "Otro": "OTRO"},
    "cole_area_ubicacion": {"Urbano": "URBANO", "Rural": "RURAL"},
    "cole_jornada": {"Única": "UNICA", "Completa": "COMPLETA", "Mañana": "MAÑANA",
                     "Tarde": "TARDE", "Noche": "NOCHE", "Sabatina": "SABATINA"},
    "cole_naturaleza": {"Oficial": 1, "No oficial": 0},
    "estu_tieneetnia": {"No": "No", "Sí": "Si"},
    "fami_educacionmadre": {"Ninguna": 0, "Primaria": 1, "Secundaria": 2,
                            "Técnica o tecnológica": 3, "Profesional o superior": 4},
    "fami_estratovivienda": {"Sin estrato": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6},
    "fami_tienecomputador": {"Sí": 1, "No": 0},
    "fami_tieneinternet": {"Sí": 1, "No": 0},
    # Código DANE del departamento del colegio
    "cole_cod_depto_ubicacion": {
        "Antioquia": 5, "Atlántico": 8, "Bogotá D.C.": 11, "Bolívar": 13, "Boyacá": 15,
        "Caldas": 17, "Caquetá": 18, "Cauca": 19, "Cesar": 20, "Córdoba": 23,
        "Cundinamarca": 25, "Chocó": 27, "Huila": 41, "La Guajira": 44, "Magdalena": 47,
        "Meta": 50, "Nariño": 52, "Norte de Santander": 54, "Quindío": 63, "Risaralda": 66,
        "Santander": 68, "Sucre": 70, "Tolima": 73, "Valle del Cauca": 76, "Arauca": 81,
        "Casanare": 85, "Putumayo": 86, "San Andrés": 88, "Amazonas": 91, "Guainía": 94,
        "Guaviare": 95, "Vaupés": 97, "Vichada": 99,
    },
}

# Variables numéricas y rangos sugeridos para los campos del formulario
NUMERICAS = {
    "estu_edad": (14, 30),
    "punt_matematicas": (0, 100),
    "punt_ingles": (0, 100),
    "punt_lectura_critica": (0, 100),
    "punt_c_naturales": (0, 100),
    "fami_cuartoshogar": (1, 10),
    "fami_personashogar": (1, 12),
}


def api_disponible() -> bool:
    try:
        return requests.get(RUTA_SALUD, timeout=5).status_code == 200
    except requests.RequestException:
        return False


def predecir(estudiante: dict) -> dict:
    """Envía un estudiante a la API y devuelve su probabilidad de no ingreso y la alerta.

    Las variables que no se envíen se tratan como faltantes y el modelo las imputa.
    Devuelve {"probabilidad", "alerta", "umbral", "version"} o {"error": mensaje}.
    """
    try:
        respuesta = requests.post(RUTA_PREDICCION, json={"inputs": [estudiante]}, timeout=30)
    except requests.RequestException as error:
        return {"error": f"No fue posible conectarse con la API ({API_URL}): {error}"}
    if respuesta.status_code != 200:
        return {"error": f"La API respondió {respuesta.status_code}: {respuesta.text[:300]}"}
    datos = respuesta.json()
    return {
        "probabilidad": datos["probabilidades"][0],
        "alerta": datos["alertas"][0],
        "umbral": datos["umbral"],
        "version": datos["version"],
    }
