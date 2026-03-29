from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Service API",
    description="Microservice for user registration, login, and profile management",
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
    return {"message": "User Service is running"}


# Register user
@app.post("/users/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password=user.password,
        phone=user.phone,
        address=user.address
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Login user
@app.post("/users/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not existing_user or existing_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "data": {
            "id": existing_user.id,
            "full_name": existing_user.full_name,
            "email": existing_user.email
        }
    }


# Get all users
@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


# Get user by ID
@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update user
@app.put("/users/{id}", response_model=schemas.UserResponse)
def update_user(id: int, updated_user: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if updated_user.email is not None:
        another_user = db.query(models.User).filter(
            models.User.email == updated_user.email,
            models.User.id != id
        ).first()
        if another_user:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = updated_user.email

    if updated_user.full_name is not None:
        user.full_name = updated_user.full_name
    if updated_user.password is not None:
        user.password = updated_user.password
    if updated_user.phone is not None:
        user.phone = updated_user.phone
    if updated_user.address is not None:
        user.address = updated_user.address

    db.commit()
    db.refresh(user)
    return user


# Delete user
@app.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}