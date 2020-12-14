import pytest
from numpy import array, dot
from numpy.linalg import norm
import pandas as pd
from src.prepare import create_cosine_matrix
from src.helpers import pivot_products, read_csv


@pytest.fixture
def df_generation():
    pytest.DF = read_csv("./data/OnlineRetail.csv")


def test_cosine_sim(df_generation):
    """retrive cosine sim for a sample of
    the data and compare with the implementation of sklearns method"""

    crosstab = pivot_products(
        ["Description"], ["CustomerID"], ["InvoiceNo"], "count", pytest.DF
    ).fillna(0.0)
    result_sample = create_cosine_matrix(crosstab).iloc[:, 0].round(3)

    def get_cosine_sim(a: pd.Series, b: pd.Series):
        """ calc the cosine sim for vectors a and b by hand"""
        a, b = array(a, dtype="float"), array(b, dtype="float")
        return dot(a, b) / (norm(a) * norm(b))

    manual_cosine_df = pd.DataFrame(
        index=list(crosstab.index), columns=list(crosstab.index)
    )
    for i in range(1):
        for j in range(len(crosstab.index)):
            manual_cosine_df.iloc[j, i] = get_cosine_sim(
                crosstab.iloc[i, :], crosstab.iloc[j, :]
            )

    expected_sample = manual_cosine_df.iloc[:, 0].astype("float64").round(3)

    print(result_sample[result_sample == expected_sample])

    assert result_sample.equals(
        expected_sample
    ), "The cosine similiarity is implemented incorrectly."
