import pandas as pd
import pytest

ESTUDIANTE_BASE = {
    "estu_edad": 17, "punt_matematicas": 62, "punt_ingles": 58, "punt_lectura_critica": 60,
    "punt_c_naturales": 55, "fami_cuartoshogar": 3, "fami_personashogar": 4,
    "estu_genero": 1, "cole_genero": "MIXTO", "cole_calendario": "A",
    "cole_area_ubicacion": "URBANO", "cole_jornada": "MAÑANA", "cole_cod_depto_ubicacion": 11,
    "estu_tieneetnia": "No", "fami_educacionmadre": 4, "fami_estratovivienda": 3,
    "fami_tienecomputador": 1, "fami_tieneinternet": 1, "cole_naturaleza": 0,
}


@pytest.fixture()
def estudiantes():
    """Dos perfiles de prueba: uno con condiciones favorables y otro con condiciones de riesgo."""
    riesgo = dict(ESTUDIANTE_BASE, punt_matematicas=35, punt_ingles=33, punt_lectura_critica=38,
                  punt_c_naturales=36, cole_area_ubicacion="RURAL", cole_jornada="SABATINA",
                  fami_educacionmadre=1, fami_estratovivienda=1, fami_tienecomputador=0,
                  fami_tieneinternet=0, cole_naturaleza=1, estu_edad=22)
    return pd.DataFrame([ESTUDIANTE_BASE, riesgo])
