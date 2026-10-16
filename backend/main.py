from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.features import (
    POST_PROCESSING_FEATURES,
    PRE_APPROVAL_FEATURES,
    engineer_transaction,
    to_model_frame,
)
from backend.schemas import PredictionResponse, TransactionInput

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models" / "production"

PRE_MODEL_PATH = MODEL_DIR / "fraud_preapproval_model.pkl"
POST_MODEL_PATH = MODEL_DIR / "fraud_postprocessing_model.pkl"

WARNING = "This is a model prediction, not a confirmed fraud finding."


def _load_model(path: Path):
    if not path.exists():
        return None
    return joblib.load(path)


preapproval_model = _load_model(PRE_MODEL_PATH)
postprocessing_model = _load_model(POST_MODEL_PATH)

app = FastAPI(
    title="Fraud Detection API",
    description=(
        "Scores transactions using the same feature pipeline as the "
        "training notebooks. /predict is the pre-approval screen."
    ),
    version="1.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _score(model, feature_names: list[str], payload: dict, model_name: str):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail=f"{model_name} model is not loaded.",
        )

    try:
        engineered = engineer_transaction(payload)
        frame = to_model_frame(engineered, feature_names)
        prediction = int(model.predict(frame)[0])
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(frame)[0][1])

    return PredictionResponse(
        model=model_name,
        prediction=prediction,
        result="Potential Fraud" if prediction == 1 else "Likely Legitimate",
        fraud_probability=probability,
        features_used=feature_names,
        warning=WARNING,
    )


@app.get("/")
def home():
    return {"message": "Fraud Detection API is running!"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "preapproval_model_loaded": preapproval_model is not None,
        "postprocessing_model_loaded": postprocessing_model is not None,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_fraud(transaction: TransactionInput):
    """Pre-approval score using only fields known before the transfer settles."""
    return _score(
        preapproval_model,
        PRE_APPROVAL_FEATURES,
        transaction.model_dump(),
        "fraud_preapproval",
    )


@app.post("/predict/post-processing", response_model=PredictionResponse)
def predict_post_processing(transaction: TransactionInput):
    """Second-stage score after sender/receiver balances are known."""
    payload = transaction.model_dump()
    if payload["Newbalanceorig"] is None or payload["Newbalancedest"] is None:
        raise HTTPException(
            status_code=422,
            detail=(
                "post-processing requires Newbalanceorig and Newbalancedest."
            ),
        )
    return _score(
        postprocessing_model,
        POST_PROCESSING_FEATURES,
        payload,
        "fraud_postprocessing",
    )
