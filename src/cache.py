from src.helpers import read_csv


class CachedData:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._sim_matrix = self._read_sim_matrix()

    def _read_sim_matrix(self):
        df = read_csv(self.file_path)
        df.set_index(df.columns[0], inplace=True)
        return df

    def get_sim_matrix(self):
        return self._sim_matrix
