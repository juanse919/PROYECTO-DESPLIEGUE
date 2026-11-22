from app.schemas.predict import MultipleDataInputs

EJEMPLO = MultipleDataInputs.model_config["json_schema_extra"]["example"]


def test_health(client):
    respuesta = client.get("/api/v1/health")
    assert respuesta.status_code == 200
    assert "model_version" in respuesta.json()


def test_predict(client):
    respuesta = client.post("/api/v1/predict", json=EJEMPLO)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["errors"] is None
    assert len(datos["probabilidades"]) == 1
    assert 0 <= datos["probabilidades"][0] <= 1
    assert datos["alertas"][0] in (0, 1)


def test_predict_entrada_invalida(client):
    malo = {"inputs": [{"punt_matematicas": "sesenta"}]}
    assert client.post("/api/v1/predict", json=malo).status_code == 422
