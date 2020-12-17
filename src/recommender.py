# import random

import pandas as pd
from toolz import curry, pipe

from src.helpers import read_csv
from src.prepare import get_user_orders

# Actual Recommendation
# TODO: try to predict purchases to evaluate params
# TODO: refactor and write tests


def generate_recommended_products(df: pd.DataFrame, user_orders: pd.DataFrame):
    """retrieve recommendations for the user's articles"""
    products = [
        df.get(ind).dropna().map(lambda x: x * user_orders.loc[ind, :][0])
        for ind in user_orders.index
    ]
    return pd.concat(products).sort_values(ascending=False)


@curry
def remove_already_bought(user_orders: pd.Series, df: pd.DataFrame):
    return df.drop(user_orders.index, axis=0, errors="ignore")


@curry
def remove_duplicates(df: pd.DataFrame):
    """ group by the dataframes index """
    return df.groupby(level=0).sum().sort_values(ascending=False)


def recommend(df: pd.DataFrame, user_orders: pd.DataFrame, item_field: str):
    """This function will be invoked by API Call -
    then add remove administrative product here"""
    return pipe(
        generate_recommended_products(df, user_orders),
        remove_already_bought(user_orders),
        remove_duplicates(),
    )


def process(
    user_orders: pd.DataFrame,
    item_field: str = "Description",
    number_options: int = 10,
):
    similiar_items = read_csv("../data/sim_matrix.csv")
    similiar_items.set_index(similiar_items.columns[0], inplace=True)
    return recommend(similiar_items, user_orders, item_field).head(number_options)


if __name__ == "__main__":
    uid = 111  # random.randint(0, 3800)
    user_orders = get_user_orders(uid=uid, item_field="Description")
    user_orders.to_json(f"./users/{uid}.json", force_ascii=False)
    print("\n--- The user ordered --- \n")
    print(user_orders.head(30))
    recommendation = process(user_orders)
    print("\n --- We would recommend ---  \n")
    print(recommendation)
