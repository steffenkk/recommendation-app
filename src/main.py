from typing import Optional, Dict
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.user import User
from src.cache import CachedData
from src.recommender import Recommender

app = FastAPI()
data = CachedData(file_path="./data/sim_matrix.csv")


@app.post("/recommendations/", response_model=User)
def get_recommendation(
    user_id: int,
    orders: Dict[str, float],
    number_options: Optional[int] = 5,
):
    user = User(id=user_id, past_orders=orders)
    recommender = Recommender(data=data, user=user)
    recommender.set_user_recommendation(number_options)

    return user


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
