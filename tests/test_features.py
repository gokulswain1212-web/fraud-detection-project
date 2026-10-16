from pytest import approx

from backend.features import (
    POST_PROCESSING_FEATURES,
    PRE_APPROVAL_FEATURES,
    engineer_transaction,
    to_model_frame,
)


def test_pre_approval_derives_sender_balance_zero():
    row = engineer_transaction(
        {
            "Step": 1,
            "Type": "payment",
            "Amount": 9839.64,
            "Oldbalanceorg": 170136.0,
            "Oldbalancedest": 0.0,
        }
    )

    assert row["Type"] == "PAYMENT"
    assert row["SenderBalanceZero"] == 0
    assert set(PRE_APPROVAL_FEATURES).issubset(row)
    frame = to_model_frame(row, PRE_APPROVAL_FEATURES)
    assert list(frame.columns) == PRE_APPROVAL_FEATURES


def test_sender_balance_zero_when_old_balance_is_zero():
    row = engineer_transaction(
        {
            "Step": 8,
            "Type": "TRANSFER",
            "Amount": 181.0,
            "Oldbalanceorg": 0.0,
            "Oldbalancedest": 21182.0,
        }
    )
    assert row["SenderBalanceZero"] == 1


def test_post_processing_matches_training_formulas():
    # First PaySim row, after the notebook-04 mismatch cleanup.
    row = engineer_transaction(
        {
            "Step": 1,
            "Type": "PAYMENT",
            "Amount": 9839.64,
            "Oldbalanceorg": 170136.0,
            "Newbalanceorig": 160296.36,
            "Oldbalancedest": 0.0,
            "Newbalancedest": 0.0,
        }
    )

    assert row["SenderBalanceChange"] == approx(9839.64)
    assert row["SenderBalanceMismatch"] == 0.0
    assert row["ReceiverBalanceChange"] == 0.0
    assert row["ReceiverBalanceMismatch"] == approx(9839.64)
    frame = to_model_frame(row, POST_PROCESSING_FEATURES)
    assert list(frame.columns) == POST_PROCESSING_FEATURES
