# Tablero: Trayectorias estudiantiles | Saber 11 → Educación Superior

Tablero en Dash que presenta el tránsito de los bachilleres desde Saber 11 hasta el ingreso a la
educación superior, siguiendo la maqueta de la Entrega 1.

## Ejecución local

Desde la carpeta `dashboard`:

```
pip install -r requirements.txt
python app.py
```

Luego abrir http://127.0.0.1:8050.

## Estructura

| Archivo | Contenido | Responsable |
|---|---|---|
| `app.py` | Aplicación, menú lateral y navegación entre páginas | Andrea Correa |
| `datos.py` | Carga de los datos agregados | Andrea Correa |
| `estilo.py`, `assets/estilo.css` | Colores y estilos de la maqueta | Andrea Correa |
| `paginas/resumen.py` | Página Resumen: indicadores, evolución por cohorte, estrato, departamento y momento del ingreso | Andrea Correa |
| `paginas/brechas.py` | Página Brechas | Paula Guarín |
| `paginas/acerca.py` | Página Acerca del proyecto | Paula Guarín |

## Datos

El tablero no lee la base completa (3,3 GB). Usa resúmenes calculados sobre los 7.138.927 registros
en `01_Exploracion_Variables.ipynb`:

- `../reports/exploracion/tasa_*.csv`: tasa de ingreso observado (`enroll_full`) por variable.
- `data/ingreso_5anios_por_cohorte.csv`: ingreso dentro de los cinco años (`enroll_5years`) por cohorte
  (sección 9.4.6 del notebook).
- `data/horizonte_ingreso.csv`: momento del ingreso (`enroll_tti`, `enroll_3years`, `enroll_5years`,
  `enroll_full`), tomado de `../reports/exploracion/consistencia_objetivo.csv`.
