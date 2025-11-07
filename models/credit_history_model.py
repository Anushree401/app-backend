# app/models/credit_history.py
from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from db import Base
import enum

class TransactionType(enum.Enum):
    ALLOCATE = "allocate"
    REDEEM = "redeem"
    TRANSFER = "transfer"

class CreditHistory(Base):
    __tablename__ = "credit_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    related_user_id = Column(String, nullable=True)
    amount = Column(Integer, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
