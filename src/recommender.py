import pandas as pd
from numpy import array
from typing import Dict

from src.cache import CachedData
from src.user import User

# Actual Recommendation


class Recommender:
    def __init__(
        self,
        data: CachedData,
        user: User,
        recommender_df: pd.DataFrame = None,
        recommended_products: Dict[str, int] = None,
    ):
        self._data = data
        self._user = user
        self._recommender_df = recommender_df
        self._recommended_products = recommended_products

    def _set_recommender_df(self):
        """retrieve recommendations for the user's articles"""
        sim_matrix = self._data.get_sim_matrix()
        arrs = {
            self._user.orderDF.index[i]: [
                array(
                    sim_matrix.get(self._user.orderDF.index[i]).dropna().index,
                    dtype="object",
                ),
                array(sim_matrix.get(self._user.orderDF.index[i]).dropna()),
            ]
            for i in range(len(self._user.orderDF.index))
        }
        products = [
            pd.Series(
                arrs[k][1] * self._user.orderDF.loc[k, :][0], index=arrs[k][0], name=k
            )
            for k, v in arrs.items()
        ]
        self._recommender_df = pd.concat(products).sort_values(ascending=False)

    def _set_recommended_products(self, number_options: int):
        """set recommendet products as dict to be serializable"""
        self._recommended_products = (
            self._recommender_df.round(2).head(number_options).to_dict()
        )

    def _remove_already_bought(self):
        """ avoid recommending already bought products """
        self._recommender_df = self._recommender_df.drop(
            self._user.orderDF.index, axis=0, errors="ignore"
        )

    def _remove_duplicates(self):
        """ group by the dataframes index """
        self._recommender_df = (
            self._recommender_df.groupby(level=0).sum().sort_values(ascending=False)
        )

    def get_recommendation(self, number_options: int):
        """This function will be invoked by API Call"""

        if not self._recommender_df:
            self._set_recommender_df()

        self._remove_already_bought()
        self._remove_duplicates()
        self._set_recommended_products(number_options=number_options)

        return self._recommended_products
