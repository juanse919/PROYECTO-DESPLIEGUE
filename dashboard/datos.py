"""Carga y preparación de los datos agregados que usa el tablero.

El tablero no lee la base completa (3,3 GB). Usa los resúmenes calculados
sobre los 7.138.927 registros en el notebook 01_Exploracion_Variables.ipynb:

- reports/exploracion/tasa_*.csv: tasa de ingreso observado (enroll_full) por variable.
- dashboard/data/ingreso_5anios_por_cohorte.csv: ingreso dentro de los cinco años
  (enroll_5years) por cohorte (sección 9.4.6 del notebook).
- dashboard/data/horizonte_ingreso.csv: momento del ingreso según los horizontes
  enroll_tti, enroll_3years, enroll_5years y enroll_full (reports/exploracion/consistencia_objetivo.csv).
"""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RUTA_EXPLORACION = RAIZ / "reports" / "exploracion"
RUTA_DATOS = Path(__file__).resolve().parent / "data"

# Último año de cohorte con cinco años completos de seguimiento (los datos llegan a 2025)
ULTIMA_COHORTE_COMPLETA = 2020

DEPARTAMENTOS = {
    5: "Antioquia", 8: "Atlántico", 11: "Bogotá D.C.", 13: "Bolívar", 15: "Boyacá",
    17: "Caldas", 18: "Caquetá", 19: "Cauca", 20: "Cesar", 23: "Córdoba",
    25: "Cundinamarca", 27: "Chocó", 41: "Huila", 44: "La Guajira", 47: "Magdalena",
    50: "Meta", 52: "Nariño", 54: "Norte de Santander", 63: "Quindío", 66: "Risaralda",
    68: "Santander", 70: "Sucre", 73: "Tolima", 76: "Valle del Cauca", 81: "Arauca",
    85: "Casanare", 86: "Putumayo", 88: "San Andrés", 91: "Amazonas", 94: "Guainía",
    95: "Guaviare", 97: "Vaupés", 99: "Vichada",
}


def _leer_tasa(variable: str) -> pd.DataFrame:
    """Lee reports/exploracion/tasa_<variable>.csv con nombres de columna uniformes."""
    tabla = pd.read_csv(RUTA_EXPLORACION / f"tasa_{variable}.csv")
    tabla = tabla.rename(columns={
        variable: "categoria",
        "Estudiantes": "estudiantes",
        "Ingresaron": "ingresaron",
        "% del total": "pct_total",
        "Tasa ingreso (%)": "tasa",
    })
    return tabla


def cargar_cohortes() -> pd.DataFrame:
    """Estudiantes, ingreso observado e ingreso en cinco años por cohorte de Saber 11."""
    observado = _leer_tasa("año").rename(columns={"categoria": "año"})
    cinco = pd.read_csv(RUTA_DATOS / "ingreso_5anios_por_cohorte.csv")
    cohortes = observado.merge(cinco[["año", "ingresaron_5anios"]], on="año", how="left")
    cohortes["tasa_5anios"] = 100 * cohortes["ingresaron_5anios"] / cohortes["estudiantes"]
    cohortes["ventana_completa"] = cohortes["año"] <= ULTIMA_COHORTE_COMPLETA
    return cohortes


def resumen_cohortes(cohortes: pd.DataFrame, desde: int, hasta: int) -> dict:
    """Indicadores agregados para un rango de cohortes."""
    sel = cohortes[cohortes["año"].between(desde, hasta)]
    estudiantes = int(sel["estudiantes"].sum())
    ingresaron = int(sel["ingresaron"].sum())
    ingresaron_5 = int(sel["ingresaron_5anios"].sum())
    return {
        "estudiantes": estudiantes,
        "tasa_observada": 100 * ingresaron / estudiantes if estudiantes else 0.0,
        "tasa_5anios": 100 * ingresaron_5 / estudiantes if estudiantes else 0.0,
        "no_ingreso_5anios": estudiantes - ingresaron_5,
        "tasa_no_ingreso_5anios": 100 * (estudiantes - ingresaron_5) / estudiantes if estudiantes else 0.0,
        "incluye_incompletas": bool((~sel["ventana_completa"]).any()),
    }


def cargar_estrato() -> pd.DataFrame:
    """Tasa de ingreso observado por estrato de la vivienda."""
    tabla = _leer_tasa("fami_estratovivienda").dropna(subset=["categoria"])
    tabla["categoria"] = tabla["categoria"].astype(int).map(
        lambda e: "Sin estrato" if e == 0 else f"Estrato {e}"
    )
    return tabla


def cargar_departamentos() -> pd.DataFrame:
    """Tasa de ingreso observado por departamento del colegio."""
    tabla = _leer_tasa("cole_cod_depto_ubicacion")
    tabla["departamento"] = tabla["categoria"].astype(int).map(DEPARTAMENTOS)
    return tabla.sort_values("tasa")


def cargar_horizonte() -> pd.DataFrame:
    """Distribución del momento de ingreso a educación superior."""
    tabla = pd.read_csv(RUTA_DATOS / "horizonte_ingreso.csv").sort_values("orden")
    tabla["pct"] = 100 * tabla["estudiantes"] / tabla["estudiantes"].sum()
    return tabla
