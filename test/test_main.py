import pytest

from src.main import get_recommendation
from src.recommender import Recommender
from src.cache import CachedData
from src.user import User


@pytest.fixture
def order_generator():
    pytest.orders = {
        "WOOD 2 DRAWER CABINET WHITE FINISH": 1.0,
        "METAL SIGN TAKE IT OR LEAVE IT ": 1.0,
        "COOK WITH WINE METAL SIGN ": 1.0,
    }


def test_get_recommendation(order_generator):
    result = get_recommendation(user_id=12, number_options=5, orders=pytest.orders)

    data = CachedData(file_path="./data/sim_matrix.csv")
    user = User(id=12, past_orders=pytest.orders)
    recommender = Recommender(data=data, user=user)

    expected = {
        "id": user.get_id(),
        "past_orders": user.get_orders(),
        "recommendations": recommender.get_recommendation(5),
    }
    assert result == expected
