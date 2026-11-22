from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

from modelo_ingreso.config.core import config
from modelo_ingreso.processing.features import LimpiezaVariables


def construir_pipeline() -> Pipeline:
    """Limpieza + imputación/escalado + One-Hot Encoding + XGBoost."""
    preprocesador = ColumnTransformer([
        ("numericas", Pipeline([
            ("imputador", SimpleImputer(strategy="median")),
            ("escalador", StandardScaler()),
        ]), config.variables_numericas),
        ("categoricas", OneHotEncoder(handle_unknown="ignore"), config.variables_categoricas),
    ])

    return Pipeline([
        ("limpieza", LimpiezaVariables(config.variables_numericas, config.variables_categoricas)),
        ("preprocesamiento", preprocesador),
        ("clasificador", XGBClassifier(
            n_estimators=config.n_estimators,
            max_depth=config.max_depth,
            learning_rate=config.learning_rate,
            subsample=config.subsample,
            colsample_bytree=config.colsample_bytree,
            objective="binary:logistic",
            eval_metric="logloss",
            tree_method="hist",
            random_state=config.semilla,
            n_jobs=2,
        )),
    ])
