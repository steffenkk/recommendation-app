import pandas as pd
import numpy as np
from pydantic import BaseModel

from typing import Dict

from src.cache import CachedData
from src.user import User

# Actual Recommendation


class Recommender(BaseModel):
    data: CachedData
    user: User
    recommender_df: pd.DataFrame = None
    recommended_products: Dict = None

    class Config:
        """ whether or not to allow custom types """

        arbitrary_types_allowed = True

    def _set_recommender_df(self):
        """retrieve recommendations for the user's articles"""
        sim_matrix = self.data.get_sim_matrix()
        arrs = {
            self.user.orderDF.index[i]: [
                np.array(
                    sim_matrix.get(self.user.orderDF.index[i]).dropna().index,
                    dtype="object",
                ),
                np.array(sim_matrix.get(self.user.orderDF.index[i]).dropna()),
            ]
            for i in range(len(self.user.orderDF.index))
        }
        products = [
            pd.Series(
                arrs[k][1] * self.user.orderDF.loc[k, :][0], index=arrs[k][0], name=k
            )
            for k, v in arrs.items()
        ]
        self.recommender_df = pd.concat(products).sort_values(ascending=False)

    def _set_recommended_products(self, number_options: int):
        """set recommendet products as dict to be serializable"""
        self.recommended_products = (
            self.recommender_df.round(2).head(number_options).to_dict()
        )

    def _remove_already_bought(self):
        """ avoid recommending already bought products """
        self.recommender_df = self.recommender_df.drop(
            self.user.orderDF.index, axis=0, errors="ignore"
        )

    def _remove_duplicates(self):
        """ group by the dataframes index """
        self.recommender_df = (
            self.recommender_df.groupby(level=0).sum().sort_values(ascending=False)
        )

    def get_recommendation(self, number_options: int):
        """This function will be invoked by API Call"""

        if not self.recommender_df:
            self._set_recommender_df()

        self._remove_already_bought()
        self._remove_duplicates()
        self._set_recommended_products(number_options=number_options)

        return self.recommended_products
