from sqlalchemy import Column, Integer, String
from database import Base

class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    driver_name = Column(String, nullable=False)
    status = Column(String, default="Preparing")
    estimated_time = Column(String, nullable=True)