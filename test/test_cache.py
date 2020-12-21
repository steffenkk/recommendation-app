from pandas import read_csv

from src.cache import CachedData


def test_cached_data():
    data = CachedData(file_path="./data/sim_matrix.csv")
    expedted = read_csv("./data/sim_matrix.csv", encoding="iso-8859-1")
    expedted.set_index(expedted.columns[0], inplace=True)
    assert data.get_sim_matrix().equals(expedted)
