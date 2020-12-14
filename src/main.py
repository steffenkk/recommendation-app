from typing import Optional, List, Dict
from fastapi import FastAPI
from src.user import User

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/recommendation/{user_id}/{order_list}")
async def get_recommendation(user_id: int, order_list: List[Dict[str:int]]):
    user = User(id=user_id, orders=order_list)
    user.set_order_df()
    return user.get_recommendation(number_ptions=5)
