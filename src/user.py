from typing import Dict
from pydantic import BaseModel


class User(BaseModel):
    id: int
    past_orders: Dict[str, int]
    recommendations: Dict[str, float] = None

    def set_recommendations(self, recommendations: Dict[str, float]):
        self.recommendations = recommendations

    def get_id(self):
        return self.id

    def get_orders(self):
        return self.past_orders

    def get_recommendation(self):
        return self.recommendations
