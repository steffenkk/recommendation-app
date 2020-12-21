import pytest
from pandas import DataFrame

from src.user import User


@pytest.fixture
def order_generator():
    pytest.orders = {
        "WOOD 2 DRAWER CABINET WHITE FINISH": 1.0,
        "METAL SIGN TAKE IT OR LEAVE IT ": 1.0,
        "COOK WITH WINE METAL SIGN ": 1.0,
    }


def test_user(order_generator):
    user = User(id=11, orders=pytest.orders)
    expected = DataFrame(index=pytest.orders.keys(), data=pytest.orders.values())
    assert user.orderDF.equals(expected)
