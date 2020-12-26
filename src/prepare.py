# prepare.py

import pandas as pd
from toolz import curry, pipe
from sklearn.metrics.pairwise import cosine_similarity

from src.helpers import read_csv, read_yaml, write_csv, pivot_products


@curry
def keep_country(country: str, df: pd.DataFrame):
    return df[df["Country"] == country]


def create_sim_matrix(
    df: pd.DataFrame, similiarity_measure: str, item_field: str, **kwargs
):
    """
    :info: create a matrix where all product vectors are compared with the
           provided similiarity_measure
    :param similiarity_measure: string, one of 'correlation' or 'cosine'
    :param kwargs: if 'correlation' you cann pass params like method or min_periods
           and method (see pandas df.corr mehtod).
           KWARGS will be ignored when 'cosine' is specified.
    """
    if similiarity_measure == "correlation":
        crosstab = pivot_products(
            ["CustomerID"], [item_field], ["InvoiceNo"], "count", df
        )
        sim_matrix = create_corr_matrix(crosstab, **kwargs).round(4)

    elif similiarity_measure == "cosine":
        crosstab = pivot_products(
            [item_field], ["CustomerID"], ["InvoiceNo"], "count", df
        ).fillna(0.0)
        sim_matrix = create_cosine_matrix(crosstab).round(4)

    else:
        raise ValueError(
            "param similiarity_measure must be one of 'correlation' or 'cosin'"
        )

    return sim_matrix


def create_corr_matrix(df: pd.DataFrame, min_periods: int, method: str = "pearson"):
    """ return a column to column correlation matrix of the given df and reindex"""
    corr_df = df.corr(method=method, min_periods=min_periods).reset_index(drop=True)
    corr_df.index = df.columns.droplevel(0).rename(None)
    corr_df.columns = df.columns.droplevel(0).rename(None)
    return corr_df


def create_cosine_matrix(df: pd.DataFrame):
    """create a matrix with the cosine similiarity of all product vectors"""
    return pd.DataFrame(
        index=list(df.index),
        columns=list(df.index),
        data=cosine_similarity(df.reset_index(drop=True)),
    )


@curry
def remove_administrative_products(adm_products: list, df: pd.DataFrame):
    return df[~df["Description"].isin(adm_products)]


@curry
def remove_zeroprice_products(df: pd.DataFrame):
    zero_pp = (
        df.groupby(["Description"])
        .UnitPrice.sum()
        .reset_index()
        .query("UnitPrice <= 0.05")["Description"]
    )
    return df[~df["Description"].isin(zero_pp)]


@curry
def remove_giftcards(df: pd.DataFrame):
    return df[~df["StockCode"].map(lambda x: str(x).startswith("gift"))]


def get_user_orders(uid: int, item_field: str):
    """ simulate a user that would come frome a rest call """
    df = prep_data("./data/OnlineRetail.csv")
    cross_tab = pivot_products(["CustomerID"], [item_field], ["InvoiceNo"], "count", df)
    return (
        cross_tab.iloc[uid]
        .dropna()
        .sort_values(ascending=False)
        .reset_index(level=0, drop=True)
    )


def prep_data(path: str):
    return pipe(
        read_csv(path),
        keep_country("United Kingdom"),
        remove_giftcards,
        remove_zeroprice_products,
        remove_administrative_products(read_yaml("./conf/meta.yaml")["admin_products"]),
    )


def process(sim_measure: str = "cosine", item_field: str = "Description", **kwargs):
    df = prep_data("./data/OnlineRetail.csv")
    similiar_items = create_sim_matrix(df, sim_measure, item_field, **kwargs)
    write_csv("./data/sim_matrix.csv", similiar_items)


if __name__ == "__main__":
    process(
        sim_measure="cosine",
        item_field="Description",
    )
