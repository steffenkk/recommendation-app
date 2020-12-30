# test_prepare.py

import pytest
import pandas as pd
from numpy import array, dot
from numpy.linalg import norm


from src.prepare import (
    create_cosine_matrix,
    create_corr_matrix,
    keep_country,
    remove_administrative_products,
    remove_zeroprice_products,
    remove_giftcards,
    prep_data,
)
from src.helpers import pivot_products, read_csv, read_yaml


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

    assert result_sample.equals(
        expected_sample
    ), "The cosine similiarity is implemented incorrectly."


def test_correlation(df_generation):
    crosstab = pivot_products(
        ["CustomerID"], ["Description"], ["InvoiceNo"], "count", pytest.DF
    )
    t_col = "ZINC T-LIGHT HOLDER STARS SMALL"
    result = (
        create_corr_matrix(crosstab, min_periods=40, method="pearson")[t_col]
        .round(3)
        .dropna()
    )

    def get_pearson_corr(x: pd.Series, y: pd.Series):
        return x.corr(y, min_periods=40, method="pearson")

    crosstab.columns = crosstab.columns.droplevel(0)
    manual_corr_df = pd.DataFrame(
        index=list(crosstab.columns),
        columns=list(crosstab.columns),
    )

    for col in manual_corr_df.index:
        manual_corr_df.loc[col, t_col] = get_pearson_corr(
            crosstab.loc[:, t_col], crosstab.loc[:, col]
        )

    expected = manual_corr_df[t_col].astype("float64").round(3).dropna()
    assert result.equals(expected)


def test_keep_country(df_generation):
    result = keep_country("United Kingdom", pytest.DF)
    assert result["Country"].all() == "United Kingdom"


def test_remove_administrative_products(df_generation):
    admin_products = read_yaml("./conf/meta.yaml")["admin_products"]
    result = remove_administrative_products(admin_products, pytest.DF)
    assert len(result["Description"].isin(admin_products).index) > 0


def test_remove_zeroprice_products(df_generation):
    result = remove_zeroprice_products(pytest.DF)
    assert (result["UnitPrice"] <= 0.05).any()


def test_prep_data(df_generation):
    path = "./data/OnlineRetail.csv"
    result = prep_data(path)
    df = read_csv(path)
    df = keep_country("United Kingdom", df)
    df = remove_giftcards(df)
    df = remove_zeroprice_products(df)
    df = remove_administrative_products(
        read_yaml("./conf/meta.yaml")["admin_products"], df
    )
    assert result.equals(df)


def test_remove_giftcards(df_generation):
    result = remove_giftcards(pytest.DF)
    assert (~result["StockCode"].map(lambda x: str(x).startswith("gift"))).any()
