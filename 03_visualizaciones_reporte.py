"""
Visualizaciones para el reporte de la Entrega 1.

Genera, a partir de las tablas agregadas de reports/exploracion/
(producidas en 02_Exploracion_Variables.ipynb), las figuras del reporte:
  - fig1_tasa_ingreso_por_grupo.png : tasa de ingreso por estrato, decil de
    matemáticas, área del colegio y acceso a internet.
  - fig2_tasa_ingreso_por_anio.png  : evolución anual de la tasa de ingreso
    (2012-2025), señalando las cohortes con seguimiento incompleto.

Uso (desde la raíz del repositorio):
    python 03_visualizaciones_reporte.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ENTRADA = Path("reports/exploracion")
SALIDA = Path("reports/figuras")
SALIDA.mkdir(parents=True, exist_ok=True)

AZUL = "#2a78d6"
GRIS = "#8a8984"
TEXTO = "#0b0b0b"
TEXTO_2 = "#52514e"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.edgecolor": "#c9c8c3",
    "axes.labelcolor": TEXTO_2,
    "xtick.color": TEXTO_2,
    "ytick.color": TEXTO_2,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def tasa_global():
    """Tasa de ingreso total (enroll_full) a partir de la tabla por año."""
    t = pd.read_csv(ENTRADA / "tasa_año.csv")
    return 100 * t["Ingresaron"].sum() / t["Estudiantes"].sum()


def panel(ax, etiquetas, tasas, titulo, ref):
    y = range(len(etiquetas))
    ax.barh(y, tasas, color=AZUL, height=0.62)
    ax.axvline(ref, color=GRIS, lw=1, ls="--")
    for yi, v in zip(y, tasas):
        ax.text(v + 1, yi, f"{v:.1f}%", va="center", fontsize=8, color=TEXTO)
    ax.set_yticks(list(y), etiquetas)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Tasa de ingreso (%)")
    ax.set_title(titulo, loc="left", fontsize=10, color=TEXTO, fontweight="bold")
    ax.grid(axis="x", color="#ecebe7", lw=0.6)
    ax.set_axisbelow(True)


def figura_1():
    ref = tasa_global()

    estrato = pd.read_csv(ENTRADA / "tasa_fami_estratovivienda.csv").dropna()
    estrato = estrato.sort_values("fami_estratovivienda")
    et_estrato = ["Sin estrato" if e == 0 else f"Estrato {int(e)}"
                  for e in estrato["fami_estratovivienda"]]

    decil = pd.read_csv(ENTRADA / "tasa_decil_matematicas.csv")
    et_decil = [f"Decil {int(d)}" for d in decil["decil_mat"]]

    area = pd.read_csv(ENTRADA / "tasa_cole_area_ubicacion.csv").dropna()
    et_area = [a.capitalize() for a in area["cole_area_ubicacion"]]

    internet = pd.read_csv(ENTRADA / "tasa_fami_tieneinternet.csv").dropna()
    et_internet = ["No" if v == 0 else "Sí" for v in internet["fami_tieneinternet"]]

    fig, axes = plt.subplots(2, 2, figsize=(10, 6.2),
                             gridspec_kw={"height_ratios": [10, 4]})
    panel(axes[0, 0], et_estrato, estrato["Tasa ingreso (%)"], "Estrato de la vivienda", ref)
    panel(axes[0, 1], et_decil, decil["enroll_full"], "Decil de puntaje en matemáticas", ref)
    panel(axes[1, 0], et_area, area["Tasa ingreso (%)"], "Área del colegio", ref)
    panel(axes[1, 1], et_internet, internet["Tasa ingreso (%)"], "Hogar con internet", ref)
    fig.text(0.01, 0.005, f"Línea punteada: tasa global de ingreso ({ref:.1f}%). "
             "Fuente: Base de Datos (MIAD), 7,1 millones de estudiantes Saber 11, 2012–2025.",
             fontsize=8, color=TEXTO_2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(SALIDA / "fig1_tasa_ingreso_por_grupo.png", dpi=200)
    plt.close(fig)


def figura_2():
    t = pd.read_csv(ENTRADA / "tasa_año.csv").sort_values("año")
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.axvspan(2020.5, 2025.5, color="#f1f0ec", zorder=0)
    ax.text(2023, 72, "Seguimiento incompleto\n(menos de 5 años observados)",
            ha="center", fontsize=8, color=TEXTO_2)
    ax.plot(t["año"], t["Tasa ingreso (%)"], color=AZUL, lw=2, marker="o", ms=5)
    for _, r in t.iterrows():
        ax.text(r["año"], r["Tasa ingreso (%)"] + 3, f"{r['Tasa ingreso (%)']:.1f}",
                ha="center", fontsize=7.5, color=TEXTO)
    ax.set_xticks(t["año"])
    ax.set_ylim(0, 82)
    ax.set_ylabel("Tasa de ingreso (%)")
    ax.set_xlabel("Año de presentación de Saber 11")
    ax.grid(axis="y", color="#ecebe7", lw=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(SALIDA / "fig2_tasa_ingreso_por_anio.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    figura_1()
    figura_2()
    print("Figuras guardadas en", SALIDA.resolve())
