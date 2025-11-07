from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import Base

class CreditHistoryDB(Base):
    __tablename__ = "credit_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users_sql.unique_id"), nullable=False)
    type = Column(String, nullable=False)  # e.g., 'credit', 'debit'
    amount = Column(Float, nullable=False)
    reason = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
