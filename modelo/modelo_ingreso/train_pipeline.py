"""Entrena el modelo, lo evalúa en validación, lo registra en MLflow y lo guarda en el paquete."""
import os

from sklearn.metrics import (accuracy_score, brier_score_loss, f1_score,
                             precision_score, recall_score, roc_auc_score)

from modelo_ingreso import __version__
from modelo_ingreso.config.core import config
from modelo_ingreso.pipeline import construir_pipeline
from modelo_ingreso.processing.data_manager import cargar_datos_modelado, guardar_pipeline


def metricas(y, probabilidades, umbral):
    pred = (probabilidades >= umbral).astype(int)
    sufijo = f"_u{int(round(umbral * 100))}"
    return {
        "accuracy" + sufijo: accuracy_score(y, pred),
        "precision" + sufijo: precision_score(y, pred, zero_division=0),
        "recall" + sufijo: recall_score(y, pred, zero_division=0),
        "f1" + sufijo: f1_score(y, pred, zero_division=0),
    }


def run_training() -> None:
    entrenamiento, validacion = cargar_datos_modelado()
    X_ent, y_ent = entrenamiento[config.variables], entrenamiento[config.objetivo]
    X_val, y_val = validacion[config.variables], validacion[config.objetivo]

    modelo = construir_pipeline()
    modelo.fit(X_ent, y_ent)
    prob_val = modelo.predict_proba(X_val)[:, 1]

    resultados = {
        "roc_auc": roc_auc_score(y_val, prob_val),
        "brier": brier_score_loss(y_val, prob_val),
        **metricas(y_val, prob_val, 0.5),
        **metricas(y_val, prob_val, config.umbral),
    }
    ruta = guardar_pipeline(modelo)

    print(f"Registros: entrenamiento {len(X_ent):,} | validación {len(X_val):,}")
    for nombre, valor in resultados.items():
        print(f"  {nombre}: {valor:.4f}")
    print(f"Modelo guardado en {ruta}")

    if os.getenv("MLFLOW_TRACKING_URI"):
        registrar_mlflow(modelo, X_val, resultados, len(X_ent), len(X_val))
    else:
        print("MLflow omitido: defina MLFLOW_TRACKING_URI para registrar el experimento.")


def registrar_mlflow(modelo, X_val, resultados, n_ent, n_val):
    import mlflow
    import mlflow.sklearn

    mlflow.set_experiment(config.nombre_experimento)
    with mlflow.start_run(run_name=f"XGBoost_paquete_v{__version__}"):
        mlflow.set_tags({"algoritmo": "XGBoost", "etapa": "Modelo empaquetado",
                         "version_paquete": __version__})
        mlflow.log_params({
            "n_estimators": config.n_estimators, "max_depth": config.max_depth,
            "learning_rate": config.learning_rate, "subsample": config.subsample,
            "colsample_bytree": config.colsample_bytree, "umbral": config.umbral,
            "fraccion_muestra": config.fraccion_muestra, "n_variables": len(config.variables),
            "registros_entrenamiento": n_ent, "registros_validacion": n_val,
        })
        mlflow.log_metrics(resultados)
        opciones = {"input_example": X_val.head(5), "serialization_format": "cloudpickle"}
        try:  # MLflow 3
            mlflow.sklearn.log_model(modelo, name="modelo", **opciones)
        except TypeError:  # MLflow 2
            mlflow.sklearn.log_model(modelo, artifact_path="modelo", **opciones)
    print("Experimento registrado en MLflow")


if __name__ == "__main__":
    run_training()
