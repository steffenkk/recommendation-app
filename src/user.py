from pydantic import BaseModel
from pandas import DataFrame
from src.recommender import process
from typing import Optional, Dict

# TODO: add recommender as class and add a new type in the user class?


class User(BaseModel):
    id: str
    orders: Optional[Dict[str, float]] = None
    orderDF: Optional[DataFrame] = None

    class Config:
        """ whether or not to allow custom types """

        arbitrary_types_allowed = True

    def set_order_df(self) -> None:
        """
        use the orders List to create a DF
        the DF then is used to retrive recommendations
        """
        orderDf = DataFrame(index=self.orders.keys(), data=self.orders.values())
        self.orderDF = orderDf

    def get_recommendation(
        self, number_ptions: int = 10, item_field: str = "Description"
    ) -> dict:
        """
        get the actual recommendation for the user from the recommender
        """
        return process(self.orderDF, item_field, number_ptions).to_dict()
