from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.main import app, postprocessing_model, preapproval_model

client = TestClient(app)

PRE_PAYLOAD = {
    "Step": 1,
    "Type": "PAYMENT",
    "Amount": 9839.64,
    "Oldbalanceorg": 170136.0,
    "Oldbalancedest": 0.0,
}

POST_PAYLOAD = {
    **PRE_PAYLOAD,
    "Newbalanceorig": 160296.36,
    "Newbalancedest": 0.0,
}

MODEL_DIR = Path(__file__).resolve().parents[1] / "models" / "production"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"


def test_predict_rejects_unknown_type():
    response = client.post(
        "/predict",
        json={**PRE_PAYLOAD, "Type": "WIRE"},
    )
    assert response.status_code == 422


def test_post_processing_requires_new_balances():
    response = client.post("/predict/post-processing", json=PRE_PAYLOAD)
    assert response.status_code == 422


@pytest.mark.skipif(
    preapproval_model is None,
    reason="pre-approval model pickle is not available",
)
def test_predict_scores_first_paysim_row_as_legitimate():
    response = client.post("/predict", json=PRE_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert body["model"] == "fraud_preapproval"
    assert body["features_used"][-1] == "SenderBalanceZero"
    assert body["prediction"] in (0, 1)
    assert body["prediction"] == 0
    assert 0.0 <= body["fraud_probability"] <= 1.0


@pytest.mark.skipif(
    postprocessing_model is None,
    reason="post-processing model pickle is not available",
)
def test_post_processing_scores_first_paysim_row_as_legitimate():
    response = client.post("/predict/post-processing", json=POST_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert body["model"] == "fraud_postprocessing"
    assert body["prediction"] == 0
