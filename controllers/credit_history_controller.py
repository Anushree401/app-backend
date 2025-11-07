# app/controllers/credit_history_controller.py
from sqlalchemy.orm import Session
from models.credit_history_model import CreditHistory, TransactionType
from io import StringIO
import csv

def create_history_entry(db: Session, user_id: str, tx_type: TransactionType, amount: int, related_user_id: str = ""):
    entry = CreditHistory(
        user_id=user_id,
        related_user_id=related_user_id,
        amount=amount,
        type=tx_type,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_user_history(db: Session, user_id: str):
    return (
        db.query(CreditHistory)
        .filter(CreditHistory.user_id == user_id)
        .order_by(CreditHistory.timestamp.desc())
        .all()
    )

def export_user_history_csv(db: Session, user_id: str):
    history = get_user_history(db, user_id)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Type", "Amount", "Related User", "Timestamp"])
    for h in history:
        writer.writerow([h.id, h.type.value, h.amount, h.related_user_id or "-", h.timestamp])
    return output.getvalue()
