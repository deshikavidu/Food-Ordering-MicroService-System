from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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


# ── Show ALL validation errors in clean format ───────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        field = error["loc"][-1]
        msg = error["msg"].replace("Value error, ", "")
        errors.append({
            "field": field,
            "message": msg
        })
    return JSONResponse(
        status_code=400,
        content={"detail": errors}
    )


# ── DB dependency ────────────────────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Root ─────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Delivery Service is running"}


# ── Create delivery ──────────────────────────────────────────────────────────
@app.post("/deliveries", response_model=schemas.DeliveryResponse, status_code=status.HTTP_201_CREATED)
def create_delivery(delivery: schemas.DeliveryCreate, db: Session = Depends(get_db)):
    try:
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
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))


# ── Get all deliveries ───────────────────────────────────────────────────────
@app.get("/deliveries", response_model=list[schemas.DeliveryResponse])
def get_all_deliveries(db: Session = Depends(get_db)):
    try:
        return db.query(models.Delivery).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))


# ── Get delivery by ID ───────────────────────────────────────────────────────
@app.get("/deliveries/{id}", response_model=schemas.DeliveryResponse)
def get_delivery(id: int, db: Session = Depends(get_db)):
    if id <= 0:
        raise HTTPException(status_code=400, detail="ID must be a positive number")
    try:
        delivery = db.query(models.Delivery).filter(models.Delivery.id == id).first()
        if not delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")
        return delivery
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))


# ── Update delivery ──────────────────────────────────────────────────────────
@app.put("/deliveries/{id}", response_model=schemas.DeliveryResponse)
def update_delivery(id: int, updated: schemas.DeliveryUpdate, db: Session = Depends(get_db)):
    if id <= 0:
        raise HTTPException(status_code=400, detail="ID must be a positive number")
    try:
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
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))