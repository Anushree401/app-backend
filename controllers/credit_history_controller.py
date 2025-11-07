import csv
import io
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from models.credit_history_model import CreditHistoryDB

async def get_credit_history(user_id: str, db: Session):
    try:
        history = db.query(CreditHistoryDB).filter(CreditHistoryDB.user_id == user_id).all()
        if not history:
            raise HTTPException(status_code=404, detail="No credit history found.")
        return {"credit_history": [
            {
                "id": h.id,
                "user_id": h.user_id,
                "type": h.type,
                "amount": h.amount,
                "reason": h.reason,
                "timestamp": h.timestamp
            } for h in history
        ]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def export_credit_history_csv(user_id: str, db: Session):
    try:
        history = db.query(CreditHistoryDB).filter(CreditHistoryDB.user_id == user_id).all()
        if not history:
            raise HTTPException(status_code=404, detail="No credit history found.")

        # Create in-memory CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "User ID", "Type", "Amount", "Reason", "Timestamp"])
        for record in history:
            writer.writerow([
                record.id,
                record.user_id,
                record.type,
                record.amount,
                record.reason,
                record.timestamp
            ])
        output.seek(0)

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=credit_history_{user_id}.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
