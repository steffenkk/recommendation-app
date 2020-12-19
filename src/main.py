from typing import Optional, Dict
from fastapi import FastAPI
import time

from src.user import User
from src.cache import CachedData
from src.recommender import Recommender

app = FastAPI()
data = CachedData(file_path="./data/sim_matrix.csv")


@app.get("/recommendations/")
def get_recommendation(user_id: int, orders: Optional[Dict[str, float]] = None):
    start_time = time.time()

    user = User(id=user_id, orders=orders)
    recommender = Recommender(data=data, user=user)

    return {
        "user_id": user.id,
        "past_orders": user.orders,
        "recommendations": recommender.get_recommendation(number_options=5),
        "exec_time": f"--- {(time.time() - start_time)} seconds ---",
    }
