from typing import Optional, Dict
from fastapi import FastAPI
from src.user import User

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/recommendations/")
def get_recommendation(user_id: int, orders: Optional[Dict[str, float]] = None):
    user = User(id=user_id, orders=orders)
    user.set_order_df()
    recommendations = user.get_recommendation(number_ptions=5)
    return {
        "user_id": user_id,
        "past_orders": orders,
        "recommendations": recommendations,
    }
