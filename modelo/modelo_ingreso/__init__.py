from pathlib import Path

PAQUETE_RAIZ = Path(__file__).resolve().parent

with open(PAQUETE_RAIZ / "VERSION") as archivo:
    __version__ = archivo.read().strip()
