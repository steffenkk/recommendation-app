import pytest
import numpy as np
import pandas as pd

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


def test_recommender(order_generator):

    data = CachedData(file_path="./data/sim_matrix.csv")
    user = User(id=12, past_orders=pytest.orders)
    recommender = Recommender(data=data, user=user)
    result = recommender.get_recommendation(10)

    # create recommendation by hand
    sim_matrix = data.get_sim_matrix()
    orderDF = pd.DataFrame(
        index=user.get_orders().keys(), data=user.get_orders().values()
    )
    arrs = {
        orderDF.index[i]: [
            np.array(
                sim_matrix.get(orderDF.index[i]).dropna().index,
                dtype="object",
            ),
            np.array(sim_matrix.get(orderDF.index[i]).dropna()),
        ]
        for i in range(len(orderDF.index))
    }
    products = [
        pd.Series(arrs[k][1] * orderDF.loc[k, :][0], index=arrs[k][0], name=k)
        for k, v in arrs.items()
    ]
    recommender_df = pd.concat(products).sort_values(ascending=False)
    recommender_df = recommender_df.drop(orderDF.index, axis=0, errors="ignore")
    expected = (
        recommender_df.groupby(level=0)
        .sum()
        .sort_values(ascending=False)
        .round(2)
        .head(10)
        .to_dict()
    )
    assert result == expected
