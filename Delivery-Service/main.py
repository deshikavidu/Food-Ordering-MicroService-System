from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Delivery Service API",
    description="Microservice for tracking delivery details and status",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Delivery Service is running"}

# Create delivery
@app.post("/deliveries", response_model=schemas.DeliveryResponse, status_code=status.HTTP_201_CREATED)
def create_delivery(delivery: schemas.DeliveryCreate, db: Session = Depends(get_db)):
    new_delivery = models.Delivery(
        order_id=delivery.order_id,
        driver_name=delivery.driver_name,
        status=delivery.status,
        estimated_time=delivery.estimated_time
    )
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)
    return new_delivery

# Get all deliveries
@app.get("/deliveries", response_model=list[schemas.DeliveryResponse])
def get_all_deliveries(db: Session = Depends(get_db)):
    return db.query(models.Delivery).all()

# Get delivery by ID
@app.get("/deliveries/{id}", response_model=schemas.DeliveryResponse)
def get_delivery(id: int, db: Session = Depends(get_db)):
    delivery = db.query(models.Delivery).filter(models.Delivery.id == id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery

# Update delivery status
@app.put("/deliveries/{id}", response_model=schemas.DeliveryResponse)
def update_delivery(id: int, updated: schemas.DeliveryUpdate, db: Session = Depends(get_db)):
    delivery = db.query(models.Delivery).filter(models.Delivery.id == id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    if updated.status is not None:
        delivery.status = updated.status
    if updated.driver_name is not None:
        delivery.driver_name = updated.driver_name
    if updated.estimated_time is not None:
        delivery.estimated_time = updated.estimated_time
    db.commit()
    db.refresh(delivery)
    return delivery