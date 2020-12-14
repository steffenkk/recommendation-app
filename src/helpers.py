import pandas as pd
from toolz import curry
from yaml import safe_load


def read_csv(file: str):
    return pd.read_csv(file, date_parser="%m/%d/%Y %H:%M", encoding="iso-8859-1")


def read_yaml(file: str):
    return safe_load(open(file))


@curry
def write_csv(file: str, df: pd.DataFrame):
    return df.to_csv(file, encoding="iso-8859-1")


def pivot_products(
    index: list, columns: list, values: list, aggfunc: str, df: pd.DataFrame
):
    return df.pivot_table(index=index, columns=columns, values=values, aggfunc=aggfunc)
