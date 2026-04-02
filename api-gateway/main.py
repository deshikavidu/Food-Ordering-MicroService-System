from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import requests

# ========================
# Pydantic Models for Request Bodies
# ========================

# User Models
class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    address: str
    
    class Config:
        example = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "1234567890",
            "address": "123 Main St"
        }


class UserLogin(BaseModel):
    email: str
    password: str
    
    class Config:
        example = {
            "email": "john@example.com",
            "password": "password123"
        }


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    
    class Config:
        example = {
            "full_name": "John Updated",
            "phone": "9876543210"
        }


# Restaurant Models
class RestaurantCreate(BaseModel):
    name: str
    location: str
    contact: str
    cuisine: str
    
    class Config:
        example = {
            "name": "MEE Hub",
            "location": "Colombo",
            "contact": "0772234567",
            "cuisine": "Sri Lankan"
        }


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    contact: Optional[str] = None
    cuisine: Optional[str] = None


class MenuItemCreate(BaseModel):
    item_name: str
    description: str
    price: float
    
    class Config:
        example = {
            "item_name": "Chocolate milkshake",
            "description": "Milky and tasty",
            "price": 450.00
        }


class MenuItemUpdate(BaseModel):
    item_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


# Order Models
class OrderItem(BaseModel):
    item_id: int
    item_name: str
    quantity: int
    price: float
    
    class Config:
        example = {
            "item_id": 101,
            "item_name": "Chicken Kottu",
            "quantity": 2,
            "price": 1200.0
        }


class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    items: List[OrderItem]
    total_amount: float
    
    class Config:
        example = {
            "user_id": 1,
            "restaurant_id": 1,
            "items": [
                {
                    "item_id": 101,
                    "item_name": "Chicken Kottu",
                    "quantity": 2,
                    "price": 1200.0
                },
                {
                    "item_id": 102,
                    "item_name": "Chocolate milkshake",
                    "quantity": 1,
                    "price": 450.0
                }
            ],
            "total_amount": 2850.0
        }


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    
    class Config:
        example = {
            "status": "Confirmed"
        }


# Payment Models
class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    method: str
    
    class Config:
        example = {
            "order_id": 1,
            "amount": 2400.0,
            "method": "Card"
        }


class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    
    class Config:
        example = {
            "status": "Refunded"
        }


# Delivery Models
class DeliveryCreate(BaseModel):
    order_id: int
    driver_name: str
    status: str = "Preparing"
    estimated_time: Optional[str] = None
    
    class Config:
        example = {
            "order_id": 1,
            "driver_name": "John Smith",
            "status": "Preparing",
            "estimated_time": "30 minutes"
        }


class DeliveryUpdate(BaseModel):
    status: Optional[str] = None
    
    class Config:
        example = {
            "status": "Out for Delivery"
        }


# Generic Request Body for flexibility
class GenericRequest(BaseModel):
    data: dict
    
    class Config:
        example = {
            "data": {}
        }

tags_metadata = [
    {
        "name": "Gateway",
        "description": "Root and general API Gateway routes"
    },
    {
        "name": "User Service",
        "description": "User registration, login, and user management routes"
    },
    {
        "name": "Restaurant Service",
        "description": "Restaurant and menu management routes"
    },
    {
        "name": "Order Service",
        "description": "Order management routes"
    },
    {
        "name": "Payment Service",
        "description": "Payment management routes"
    },
    {
        "name": "Delivery Service",
        "description": "Delivery tracking and management routes"
    }
]

app = FastAPI(
    title="API Gateway",
    description="Gateway for Online Food Ordering Microservices",
    version="1.0.0",
    openapi_tags=tags_metadata
)

# -------------------------
# Service URLs
# -------------------------
USER_SERVICE = "http://127.0.0.1:8001"
RESTAURANT_SERVICE = "http://127.0.0.1:8002"
ORDER_SERVICE = "http://127.0.0.1:8003"
PAYMENT_SERVICE = "http://127.0.0.1:8004"
DELIVERY_SERVICE = "http://127.0.0.1:8005"


# -------------------------
# Root Route
# -------------------------
@app.get("/", tags=["Gateway"], summary="Gateway Root")
def root():
    return {"message": "API Gateway is running"}


# -------------------------
# Helper function
# -------------------------
def forward_request(method: str, url: str, body=None):
    try:
        # Send request to microservice
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=body, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=body, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, timeout=5)
        else:
            return JSONResponse(
                status_code=405,
                content={"error": "Method not allowed"}
            )

        # Try to parse response as JSON, if it fails, return text
        try:
            response_data = response.json()
        except:
            response_data = {"message": response.text} if response.text else {}

        return JSONResponse(
            status_code=response.status_code,
            content=response_data
        )

    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error to {url}: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"error": f"Service unavailable at {url}"}
        )
    except requests.exceptions.Timeout:
        print(f"Timeout connecting to {url}")
        return JSONResponse(
            status_code=504,
            content={"error": f"Service timeout at {url}"}
        )
    except Exception as e:
        print(f"Error in forward_request: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal error: {str(e)}"}
        )


# =========================
# USER SERVICE ROUTES
# =========================
@app.post("/users/register", tags=["User Service"], summary="Register User")
def register_user(user: UserRegister):
    body = user.dict()
    return forward_request("POST", f"{USER_SERVICE}/users/register", body)


@app.post("/users/login", tags=["User Service"], summary="Login User")
def login_user(user: UserLogin):
    body = user.dict()
    return forward_request("POST", f"{USER_SERVICE}/users/login", body)


@app.get("/users", tags=["User Service"], summary="Get Users")
def get_users():
    return forward_request("GET", f"{USER_SERVICE}/users")


@app.get("/users/{id}", tags=["User Service"], summary="Get User By Id")
def get_user_by_id(id: int):
    return forward_request("GET", f"{USER_SERVICE}/users/{id}")


@app.put("/users/{id}", tags=["User Service"], summary="Update User")
def update_user(id: int, user: UserUpdate):
    body = user.dict(exclude_none=True)
    return forward_request("PUT", f"{USER_SERVICE}/users/{id}", body)


@app.delete("/users/{id}", tags=["User Service"], summary="Delete User")
def delete_user(id: int):
    return forward_request("DELETE", f"{USER_SERVICE}/users/{id}")


# =========================
# RESTAURANT SERVICE ROUTES
# =========================
@app.get("/restaurants", tags=["Restaurant Service"], summary="Get Restaurants")
def get_restaurants():
    return forward_request("GET", f"{RESTAURANT_SERVICE}/restaurants")


@app.post("/restaurants", tags=["Restaurant Service"], summary="Create Restaurant")
def create_restaurant(restaurant: RestaurantCreate):
    body = restaurant.dict()
    return forward_request("POST", f"{RESTAURANT_SERVICE}/restaurants", body)


@app.get("/restaurants/{id}", tags=["Restaurant Service"], summary="Get Restaurant By Id")
def get_restaurant_by_id(id: int):
    return forward_request("GET", f"{RESTAURANT_SERVICE}/restaurants/{id}")


@app.put("/restaurants/{id}", tags=["Restaurant Service"], summary="Update Restaurant")
def update_restaurant(id: int, restaurant: RestaurantUpdate):
    body = restaurant.dict(exclude_none=True)
    return forward_request("PUT", f"{RESTAURANT_SERVICE}/restaurants/{id}", body)


@app.delete("/restaurants/{id}", tags=["Restaurant Service"], summary="Delete Restaurant")
def delete_restaurant(id: int):
    return forward_request("DELETE", f"{RESTAURANT_SERVICE}/restaurants/{id}")


@app.post("/restaurants/{id}/menu", tags=["Restaurant Service"], summary="Add Menu Item")
def add_menu_item(id: int, item: MenuItemCreate):
    body = item.dict()
    return forward_request("POST", f"{RESTAURANT_SERVICE}/restaurants/{id}/menu", body)


@app.get("/restaurants/{id}/menu", tags=["Restaurant Service"], summary="Get Restaurant Menu")
def get_menu(id: int):
    return forward_request("GET", f"{RESTAURANT_SERVICE}/restaurants/{id}/menu")


@app.put(
    "/restaurants/{restaurant_id}/menu/{item_id}",
    tags=["Restaurant Service"],
    summary="Update Menu Item"
)
def update_menu_item(restaurant_id: int, item_id: int, item: MenuItemUpdate):
    body = item.dict(exclude_none=True)
    return forward_request(
        "PUT",
        f"{RESTAURANT_SERVICE}/restaurants/{restaurant_id}/menu/{item_id}",
        body
    )


@app.delete(
    "/restaurants/{restaurant_id}/menu/{item_id}",
    tags=["Restaurant Service"],
    summary="Delete Menu Item"
)
def delete_menu_item(restaurant_id: int, item_id: int):
    return forward_request(
        "DELETE",
        f"{RESTAURANT_SERVICE}/restaurants/{restaurant_id}/menu/{item_id}"
    )


# =========================
# ORDER SERVICE ROUTES
# =========================
@app.post("/orders", tags=["Order Service"], summary="Create Order")
def create_order(order: OrderCreate):
    body = order.dict()
    return forward_request("POST", f"{ORDER_SERVICE}/orders", body)


@app.get("/orders", tags=["Order Service"], summary="Get Orders")
def get_orders():
    return forward_request("GET", f"{ORDER_SERVICE}/orders")


@app.get("/orders/{id}", tags=["Order Service"], summary="Get Order By Id")
def get_order_by_id(id: int):
    return forward_request("GET", f"{ORDER_SERVICE}/orders/{id}")


@app.put("/orders/{id}", tags=["Order Service"], summary="Update Order")
def update_order(id: int, order: OrderUpdate):
    body = order.dict(exclude_none=True)
    return forward_request("PUT", f"{ORDER_SERVICE}/orders/{id}", body)


@app.delete("/orders/{id}", tags=["Order Service"], summary="Delete Order")
def delete_order(id: int):
    return forward_request("DELETE", f"{ORDER_SERVICE}/orders/{id}")


# =========================
# PAYMENT SERVICE ROUTES
# =========================
@app.post("/payments", tags=["Payment Service"], summary="Create Payment")
def create_payment(payment: PaymentCreate):
    body = payment.dict()
    return forward_request("POST", f"{PAYMENT_SERVICE}/payments", body)


@app.get("/payments", tags=["Payment Service"], summary="Get Payments")
def get_payments():
    return forward_request("GET", f"{PAYMENT_SERVICE}/payments")


@app.get("/payments/{id}", tags=["Payment Service"], summary="Get Payment By Id")
def get_payment_by_id(id: int):
    return forward_request("GET", f"{PAYMENT_SERVICE}/payments/{id}")


@app.put("/payments/{id}", tags=["Payment Service"], summary="Update Payment")
def update_payment(id: int, payment: PaymentUpdate):
    body = payment.dict(exclude_none=True)
    return forward_request("PUT", f"{PAYMENT_SERVICE}/payments/{id}", body)


@app.delete("/payments/{id}", tags=["Payment Service"], summary="Delete Payment")
def delete_payment(id: int):
    return forward_request("DELETE", f"{PAYMENT_SERVICE}/payments/{id}")


# =========================
# DELIVERY SERVICE ROUTES
# =========================
@app.post("/deliveries", tags=["Delivery Service"], summary="Create Delivery")
def create_delivery(delivery: DeliveryCreate):
    body = delivery.dict()
    return forward_request("POST", f"{DELIVERY_SERVICE}/deliveries", body)


@app.get("/deliveries", tags=["Delivery Service"], summary="Get Deliveries")
def get_deliveries():
    return forward_request("GET", f"{DELIVERY_SERVICE}/deliveries")


@app.get("/deliveries/{id}", tags=["Delivery Service"], summary="Get Delivery By Id")
def get_delivery_by_id(id: int):
    return forward_request("GET", f"{DELIVERY_SERVICE}/deliveries/{id}")


@app.put("/deliveries/{id}", tags=["Delivery Service"], summary="Update Delivery")
def update_delivery(id: int, delivery: DeliveryUpdate):
    body = delivery.dict(exclude_none=True)
    return forward_request("PUT", f"{DELIVERY_SERVICE}/deliveries/{id}", body)


@app.delete("/deliveries/{id}", tags=["Delivery Service"], summary="Delete Delivery")
def delete_delivery(id: int):
    return forward_request("DELETE", f"{DELIVERY_SERVICE}/deliveries/{id}")