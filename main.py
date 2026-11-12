from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

restaurants = []


class Restaurant(BaseModel):
    name: str
    location: str

class MenuItem(BaseModel):
    name: str
    price: float


@app.get("/")
def home():
    return {"message": "Restaurant Service is running"}


@app.post("/restaurants")
def create_restaurant(restaurant: Restaurant):
    restaurant_data = {
        "id": len(restaurants) + 1,
        "name": restaurant.name,
        "location": restaurant.location
    }

    restaurants.append(restaurant_data)

    return restaurant_data

@app.get("/restaurants")
def get_restaurants():
    return restaurants

@app.post("/restaurants/{restaurant_id}/menu")
def add_menu_item(restaurant_id: int, menu_item: MenuItem):
    for restaurant in restaurants:
        if restaurant["id"] == restaurant_id:
            if "menu" not in restaurant:
                restaurant["menu"] = []

            menu_data = {
                "id": len(restaurant["menu"]) + 1,
                "name": menu_item.name,
                "price": menu_item.price
            }

            restaurant["menu"].append(menu_data)

            return menu_data

    return {"error": "Restaurant not found"}

@app.get("/restaurants/{restaurant_id}/menu")
def get_menu(restaurant_id: int):
    for restaurant in restaurants:
        if restaurant["id"] == restaurant_id:
            return restaurant.get("menu", [])

    return {"error": "Restaurant not found"}