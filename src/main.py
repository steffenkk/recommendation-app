from typing import Optional, Dict
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import time

from src.user import User
from src.cache import CachedData
from src.recommender import Recommender

app = FastAPI()
data = CachedData(file_path="./data/sim_matrix.csv")


@app.get("/recommendations/")
def get_recommendation(
    user_id: int,
    number_options: Optional[int] = 10,
    orders: Optional[Dict[str, float]] = None,
):
    start_time = time.time()

    user = User(id=user_id, orders=orders)
    recommender = Recommender(data=data, user=user)

    return {
        "user_id": user.id,
        "past_orders": user.orders,
        "recommendations": recommender.get_recommendation(number_options),
        "exec_time": f"--- {(time.time() - start_time)} seconds ---",
    }


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Service for product recommendations",
        version="0.0.1",
        description="Custom Open API Schema for the recommendation app",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
