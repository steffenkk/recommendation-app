import pytest

from src.user import User


@pytest.fixture
def order_generator():
    pytest.orders = {
        "WOOD 2 DRAWER CABINET WHITE FINISH": 1,
        "METAL SIGN TAKE IT OR LEAVE IT ": 1,
        "COOK WITH WINE METAL SIGN ": 1,
    }


def test_user(order_generator):
    user = User(id=11, past_orders=pytest.orders)
    expected = {
        "id": 11,
        "past_orders": pytest.orders,
        "recommendations": None,
    }
    assert user == expected
