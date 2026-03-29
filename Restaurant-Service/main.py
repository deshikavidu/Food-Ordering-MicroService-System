from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant Service API",
    description="Microservice for managing restaurants and menus",
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
    return {"message": "Restaurant Service is running"}


# -------------------------------
# Restaurant APIs
# -------------------------------

@app.get("/restaurants", response_model=list[schemas.RestaurantResponse])
def get_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(models.Restaurant).all()
    return restaurants


@app.post(
    "/restaurants",
    response_model=schemas.RestaurantResponse,
    status_code=status.HTTP_201_CREATED
)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    new_restaurant = models.Restaurant(
        name=restaurant.name,
        location=restaurant.location,
        contact=restaurant.contact,
        cuisine=restaurant.cuisine
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant


@app.get("/restaurants/{id}", response_model=schemas.RestaurantWithMenuResponse)
def get_restaurant_by_id(id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@app.put("/restaurants/{id}", response_model=schemas.RestaurantResponse)
def update_restaurant(id: int, restaurant: schemas.RestaurantUpdate, db: Session = Depends(get_db)):
    existing_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id).first()
    if not existing_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    if restaurant.name is not None:
        existing_restaurant.name = restaurant.name
    if restaurant.location is not None:
        existing_restaurant.location = restaurant.location
    if restaurant.contact is not None:
        existing_restaurant.contact = restaurant.contact
    if restaurant.cuisine is not None:
        existing_restaurant.cuisine = restaurant.cuisine

    db.commit()
    db.refresh(existing_restaurant)
    return existing_restaurant


@app.delete("/restaurants/{id}")
def delete_restaurant(id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    db.delete(restaurant)
    db.commit()
    return {"message": "Restaurant deleted successfully"}


# -------------------------------
# Menu APIs
# -------------------------------

@app.post(
    "/restaurants/{id}/menu",
    response_model=schemas.MenuItemResponse,
    status_code=status.HTTP_201_CREATED
)
def add_menu_item(id: int, menu_item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    new_item = models.MenuItem(
        item_name=menu_item.item_name,
        price=menu_item.price,
        description=menu_item.description,
        restaurant_id=id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/restaurants/{id}/menu", response_model=list[schemas.MenuItemResponse])
def get_menu(id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    menu_items = db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == id).all()
    return menu_items


@app.put("/restaurants/{restaurant_id}/menu/{item_id}", response_model=schemas.MenuItemResponse)
def update_menu_item(
    restaurant_id: int,
    item_id: int,
    menu_item: schemas.MenuItemUpdate,
    db: Session = Depends(get_db)
):
    existing_item = db.query(models.MenuItem).filter(
        models.MenuItem.id == item_id,
        models.MenuItem.restaurant_id == restaurant_id
    ).first()

    if not existing_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    if menu_item.item_name is not None:
        existing_item.item_name = menu_item.item_name
    if menu_item.price is not None:
        existing_item.price = menu_item.price
    if menu_item.description is not None:
        existing_item.description = menu_item.description

    db.commit()
    db.refresh(existing_item)
    return existing_item


@app.delete("/restaurants/{restaurant_id}/menu/{item_id}")
def delete_menu_item(restaurant_id: int, item_id: int, db: Session = Depends(get_db)):
    existing_item = db.query(models.MenuItem).filter(
        models.MenuItem.id == item_id,
        models.MenuItem.restaurant_id == restaurant_id
    ).first()

    if not existing_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    db.delete(existing_item)
    db.commit()
    return {"message": "Menu item deleted successfully"}