"""Feature engineering that matches notebook 04 (the formulas used to train)."""

from __future__ import annotations

from typing import Mapping

import pandas as pd

TRANSACTION_TYPES = (
    "CASH_IN",
    "CASH_OUT",
    "DEBIT",
    "PAYMENT",
    "TRANSFER",
)

PRE_APPROVAL_FEATURES = [
    "Step",
    "Type",
    "Amount",
    "Oldbalanceorg",
    "Oldbalancedest",
    "SenderBalanceZero",
]

POST_PROCESSING_FEATURES = [
    "Step",
    "Type",
    "Amount",
    "Oldbalanceorg",
    "Newbalanceorig",
    "Oldbalancedest",
    "Newbalancedest",
    "SenderBalanceChange",
    "SenderBalanceMismatch",
    "ReceiverBalanceChange",
    "ReceiverBalanceMismatch",
    "SenderBalanceZero",
]

_FLOAT_ZERO_EPS = 1e-8


def _zero_tiny(value: float) -> float:
    abs_value = abs(float(value))
    return 0.0 if abs_value <= _FLOAT_ZERO_EPS else abs_value


def normalize_type(transaction_type: str) -> str:
    return str(transaction_type).strip().upper()


def sender_balance_zero(old_balance_org: float) -> int:
    return int(float(old_balance_org) == 0)


def engineer_transaction(payload: Mapping) -> dict:
    """Build the engineered row used by both production models."""
    step = int(payload["Step"])
    amount = float(payload["Amount"])
    old_org = float(payload["Oldbalanceorg"])
    old_dest = float(payload["Oldbalancedest"])
    txn_type = normalize_type(payload["Type"])

    new_org = payload.get("Newbalanceorig")
    new_dest = payload.get("Newbalancedest")

    row = {
        "Step": step,
        "Type": txn_type,
        "Amount": amount,
        "Oldbalanceorg": old_org,
        "Oldbalancedest": old_dest,
        "SenderBalanceZero": sender_balance_zero(old_org),
    }

    if new_org is None or new_dest is None:
        return row

    new_org = float(new_org)
    new_dest = float(new_dest)
    sender_change = old_org - new_org
    receiver_change = new_dest - old_dest

    row.update(
        {
            "Newbalanceorig": new_org,
            "Newbalancedest": new_dest,
            "SenderBalanceChange": sender_change,
            "SenderBalanceMismatch": _zero_tiny(sender_change - amount),
            "ReceiverBalanceChange": receiver_change,
            "ReceiverBalanceMismatch": _zero_tiny(receiver_change - amount),
        }
    )
    return row


def to_model_frame(row: Mapping, feature_names: list[str]) -> pd.DataFrame:
    missing = [name for name in feature_names if name not in row]
    if missing:
        raise ValueError(
            "Missing fields required by the model: " + ", ".join(missing)
        )
    return pd.DataFrame([{name: row[name] for name in feature_names}])
