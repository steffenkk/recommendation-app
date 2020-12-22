from pandas import DataFrame
from typing import Dict


class User:
    def __init__(self, id: int, orders: Dict[str, int]):
        """
        use the orders List to create a DF
        the DF then is used to retrive recommendations
        """
        self.id = id
        self.orders = orders
        self.orderDF = DataFrame(index=orders.keys(), data=orders.values())

    def get_id(self):
        return self.id

    def get_orders(self):
        return self.orders
