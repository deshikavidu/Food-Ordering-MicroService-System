from sqlalchemy import Column, Integer, Float, String
from database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String, nullable=False)   # e.g. "Card", "Cash"
    status = Column(String, default="Paid")   # e.g. "Paid", "Refunded"