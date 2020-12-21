from typing import Optional
from pandas import DataFrame

from src.helpers import read_csv


class CachedData:
    def __init__(
        self, file_path: Optional[str] = None, sim_matrix: Optional[DataFrame] = None
    ):
        if file_path is not None or sim_matrix is not None:
            self.file_path = file_path
            self.sim_matrix = (
                sim_matrix if sim_matrix is not None else self._read_sim_matrix()
            )
        else:
            raise AttributeError("One of file_path and sim_matrix must be provided ")

    def _read_sim_matrix(self):
        df = read_csv(self.file_path)
        df.set_index(df.columns[0], inplace=True)
        return df

    def get_sim_matrix(self):
        return self.sim_matrix
