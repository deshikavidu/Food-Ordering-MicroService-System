from sqlalchemy import Column, Integer, String, Float, Text
from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    restaurant_id = Column(Integer, nullable=False)
    items = Column(Text, nullable=False)       # stored as JSON string
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="Pending")