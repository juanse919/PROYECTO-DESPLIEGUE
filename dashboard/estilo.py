"""Colores y formato común de las gráficas (tomados de la maqueta)."""

AZUL_OSCURO = "#14394A"
AZUL = "#1F5F7A"
TURQUESA = "#2A9D9A"
TURQUESA_CLARO = "#9FD6D2"
AMARILLO = "#F2C14E"
GRIS = "#6B7C85"
GRIS_CLARO = "#E3EAED"
FUENTE = "Segoe UI, Inter, Helvetica, Arial, sans-serif"


def aplicar_formato(fig, alto: int = 320):
    """Aplica el formato común: fondo transparente, fuente y márgenes compactos."""
    fig.update_layout(
        height=alto,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FUENTE, size=12, color=AZUL_OSCURO),
        hoverlabel=dict(font_family=FUENTE),
        legend=dict(orientation="h", yanchor="top", y=-0.15, x=0),
    )
    fig.update_xaxes(gridcolor=GRIS_CLARO, zeroline=False)
    fig.update_yaxes(gridcolor=GRIS_CLARO, zeroline=False)
    return fig


def formato_numero(valor: float, decimales: int = 0) -> str:
    """Formato colombiano: punto para miles y coma para decimales."""
    texto = f"{valor:,.{decimales}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")
