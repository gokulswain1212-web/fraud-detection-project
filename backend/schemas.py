from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from backend.features import TRANSACTION_TYPES, normalize_type

TransactionType = Literal[
    "CASH_IN",
    "CASH_OUT",
    "DEBIT",
    "PAYMENT",
    "TRANSFER",
]


class TransactionInput(BaseModel):
    """Raw transaction fields. Engineered columns are derived in code."""

    Step: int = Field(ge=0)
    Type: TransactionType
    Amount: float = Field(ge=0)
    Oldbalanceorg: float = Field(ge=0)
    Oldbalancedest: float = Field(ge=0)
    Newbalanceorig: Optional[float] = Field(default=None, ge=0)
    Newbalancedest: Optional[float] = Field(default=None, ge=0)

    @field_validator("Type", mode="before")
    @classmethod
    def uppercase_type(cls, value: str) -> str:
        normalized = normalize_type(value)
        if normalized not in TRANSACTION_TYPES:
            allowed = ", ".join(TRANSACTION_TYPES)
            raise ValueError(f"Type must be one of: {allowed}")
        return normalized


class PredictionResponse(BaseModel):
    model: str
    prediction: int
    result: str
    fraud_probability: Optional[float]
    features_used: list[str]
    warning: str
