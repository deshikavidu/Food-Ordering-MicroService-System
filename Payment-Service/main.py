from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Payment Service API",
    description="Microservice for handling payment processing and status",
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
    return {"message": "Payment Service is running"}


# --------------------------------
# Payment APIs
# --------------------------------

@app.post("/payments", response_model=schemas.PaymentResponse, status_code=status.HTTP_201_CREATED)
def make_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    new_payment = models.Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        method=payment.method,
        status="Paid"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@app.get("/payments", response_model=list[schemas.PaymentResponse])
def get_all_payments(db: Session = Depends(get_db)):
    return db.query(models.Payment).all()


@app.get("/payments/{id}", response_model=schemas.PaymentResponse)
def get_payment_by_id(id: int, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@app.put("/payments/{id}", response_model=schemas.PaymentResponse)
def update_payment_status(id: int, updated: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if updated.status is not None:
        payment.status = updated.status
    db.commit()
    db.refresh(payment)
    return payment