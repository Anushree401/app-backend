from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from controllers.credit_history_controller import get_credit_history, export_credit_history_csv

router = APIRouter(prefix="/credit-history", tags=["Credit History"])

@router.get("/{user_id}")
async def fetch_credit_history(user_id: str, db: Session = Depends(get_db)):
    return await get_credit_history(user_id, db)

@router.get("/{user_id}/export")
async def export_credit_history(user_id: str, db: Session = Depends(get_db)):
    return await export_credit_history_csv(user_id, db)
