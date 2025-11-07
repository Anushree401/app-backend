# app/routes/credit_history_routes.py
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from db import get_db
from controllers.credit_history_controller import (
    get_user_history,
    export_user_history_csv,
)

router = APIRouter(prefix="/history", tags=["Credit History"])

@router.get("/{user_id}")
def get_history(user_id: str, db: Session = Depends(get_db)):
    return get_user_history(db, user_id)

@router.get("/{user_id}/export")
def export_history(user_id: str, db: Session = Depends(get_db)):
    csv_data = export_user_history_csv(db, user_id)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=credit_history_{user_id}.csv"}
    )
