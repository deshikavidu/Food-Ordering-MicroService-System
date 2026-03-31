from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests

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
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=body)
        elif method == "PUT":
            response = requests.put(url, json=body)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            return JSONResponse(
                status_code=405,
                content={"error": "Method not allowed"}
            )

        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )

    except requests.exceptions.ConnectionError:
        return JSONResponse(
            status_code=503,
            content={"error": f"Service unavailable for URL: {url}"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# =========================
# USER SERVICE ROUTES
# =========================
@app.post("/users/register", tags=["User Service"], summary="Register User")
async def register_user(request: Request):
    body = await request.json()
    return forward_request("POST", f"{USER_SERVICE}/users/register", body)


@app.post("/users/login", tags=["User Service"], summary="Login User")
async def login_user(request: Request):
    body = await request.json()
    return forward_request("POST", f"{USER_SERVICE}/users/login", body)


@app.get("/users", tags=["User Service"], summary="Get Users")
def get_users():
    return forward_request("GET", f"{USER_SERVICE}/users")


@app.get("/users/{id}", tags=["User Service"], summary="Get User By Id")
def get_user_by_id(id: int):
    return forward_request("GET", f"{USER_SERVICE}/users/{id}")


@app.put("/users/{id}", tags=["User Service"], summary="Update User")
async def update_user(id: int, request: Request):
    body = await request.json()
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
async def create_restaurant(request: Request):
    body = await request.json()
    return forward_request("POST", f"{RESTAURANT_SERVICE}/restaurants", body)


@app.get("/restaurants/{id}", tags=["Restaurant Service"], summary="Get Restaurant By Id")
def get_restaurant_by_id(id: int):
    return forward_request("GET", f"{RESTAURANT_SERVICE}/restaurants/{id}")


@app.put("/restaurants/{id}", tags=["Restaurant Service"], summary="Update Restaurant")
async def update_restaurant(id: int, request: Request):
    body = await request.json()
    return forward_request("PUT", f"{RESTAURANT_SERVICE}/restaurants/{id}", body)


@app.delete("/restaurants/{id}", tags=["Restaurant Service"], summary="Delete Restaurant")
def delete_restaurant(id: int):
    return forward_request("DELETE", f"{RESTAURANT_SERVICE}/restaurants/{id}")


@app.post("/restaurants/{id}/menu", tags=["Restaurant Service"], summary="Add Menu Item")
async def add_menu_item(id: int, request: Request):
    body = await request.json()
    return forward_request("POST", f"{RESTAURANT_SERVICE}/restaurants/{id}/menu", body)


@app.get("/restaurants/{id}/menu", tags=["Restaurant Service"], summary="Get Restaurant Menu")
def get_menu(id: int):
    return forward_request("GET", f"{RESTAURANT_SERVICE}/restaurants/{id}/menu")


@app.put(
    "/restaurants/{restaurant_id}/menu/{item_id}",
    tags=["Restaurant Service"],
    summary="Update Menu Item"
)
async def update_menu_item(restaurant_id: int, item_id: int, request: Request):
    body = await request.json()
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
async def create_order(request: Request):
    body = await request.json()
    return forward_request("POST", f"{ORDER_SERVICE}/orders", body)


@app.get("/orders", tags=["Order Service"], summary="Get Orders")
def get_orders():
    return forward_request("GET", f"{ORDER_SERVICE}/orders")


@app.get("/orders/{id}", tags=["Order Service"], summary="Get Order By Id")
def get_order_by_id(id: int):
    return forward_request("GET", f"{ORDER_SERVICE}/orders/{id}")


@app.put("/orders/{id}", tags=["Order Service"], summary="Update Order")
async def update_order(id: int, request: Request):
    body = await request.json()
    return forward_request("PUT", f"{ORDER_SERVICE}/orders/{id}", body)


@app.delete("/orders/{id}", tags=["Order Service"], summary="Delete Order")
def delete_order(id: int):
    return forward_request("DELETE", f"{ORDER_SERVICE}/orders/{id}")


# =========================
# PAYMENT SERVICE ROUTES
# =========================
@app.post("/payments", tags=["Payment Service"], summary="Create Payment")
async def create_payment(request: Request):
    body = await request.json()
    return forward_request("POST", f"{PAYMENT_SERVICE}/payments", body)


@app.get("/payments", tags=["Payment Service"], summary="Get Payments")
def get_payments():
    return forward_request("GET", f"{PAYMENT_SERVICE}/payments")


@app.get("/payments/{id}", tags=["Payment Service"], summary="Get Payment By Id")
def get_payment_by_id(id: int):
    return forward_request("GET", f"{PAYMENT_SERVICE}/payments/{id}")


@app.put("/payments/{id}", tags=["Payment Service"], summary="Update Payment")
async def update_payment(id: int, request: Request):
    body = await request.json()
    return forward_request("PUT", f"{PAYMENT_SERVICE}/payments/{id}", body)


@app.delete("/payments/{id}", tags=["Payment Service"], summary="Delete Payment")
def delete_payment(id: int):
    return forward_request("DELETE", f"{PAYMENT_SERVICE}/payments/{id}")


# =========================
# DELIVERY SERVICE ROUTES
# =========================
@app.post("/deliveries", tags=["Delivery Service"], summary="Create Delivery")
async def create_delivery(request: Request):
    body = await request.json()
    return forward_request("POST", f"{DELIVERY_SERVICE}/deliveries", body)


@app.get("/deliveries", tags=["Delivery Service"], summary="Get Deliveries")
def get_deliveries():
    return forward_request("GET", f"{DELIVERY_SERVICE}/deliveries")


@app.get("/deliveries/{id}", tags=["Delivery Service"], summary="Get Delivery By Id")
def get_delivery_by_id(id: int):
    return forward_request("GET", f"{DELIVERY_SERVICE}/deliveries/{id}")


@app.put("/deliveries/{id}", tags=["Delivery Service"], summary="Update Delivery")
async def update_delivery(id: int, request: Request):
    body = await request.json()
    return forward_request("PUT", f"{DELIVERY_SERVICE}/deliveries/{id}", body)


@app.delete("/deliveries/{id}", tags=["Delivery Service"], summary="Delete Delivery")
def delete_delivery(id: int):
    return forward_request("DELETE", f"{DELIVERY_SERVICE}/deliveries/{id}")