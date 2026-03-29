import json
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Order Service API",
    description="Microservice for order placement and order tracking",
    version="1.0.0"
)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Order Service is running"}


# --------------------------------
# Order APIs
# --------------------------------

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def place_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    items_json = json.dumps([item.dict() for item in order.items])

    new_order = models.Order(
        user_id=order.user_id,
        restaurant_id=order.restaurant_id,
        items=items_json,
        total_amount=order.total_amount,
        status="Pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "message": "Order placed successfully",
        "data": {
            "order_id": new_order.id,
            "status": new_order.status
        }
    }


@app.get("/orders")
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return {
        "message": "Orders retrieved successfully",
        "data": orders
    }


@app.get("/orders/{id}")
def get_order_by_id(id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "message": "Order retrieved successfully",
        "data": order
    }


@app.put("/orders/{id}")
def update_order_status(id: int, updated: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if updated.status is not None:
        order.status = updated.status

    db.commit()
    db.refresh(order)

    return {
        "message": "Order status updated successfully",
        "data": {
            "order_id": order.id,
            "status": order.status
        }
    }

@app.delete("/orders/{id}")
def delete_order(id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}