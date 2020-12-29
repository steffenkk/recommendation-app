import pandas as pd
from numpy import array

from src.cache import CachedData
from src.user import User

# Actual Recommendation


class Recommender:
    def __init__(
        self,
        data: CachedData,
        user: User,
        recommender_df: pd.DataFrame = None,
    ):
        self._data = data
        self._user = user
        self._order_df = pd.DataFrame(
            index=user.get_orders().keys(), data=user.get_orders().values()
        )
        self._recommender_df = recommender_df

    def _set_recommender_df(self):
        """retrieve recommendations for the user's articles"""
        sim_matrix = self._data.get_sim_matrix()
        arrs = {
            self._order_df.index[i]: [
                array(
                    sim_matrix.get(self._order_df.index[i]).dropna().index,
                    dtype="object",
                ),
                array(sim_matrix.get(self._order_df.index[i]).dropna()),
            ]
            for i in range(len(self._order_df.index))
        }
        products = [
            pd.Series(
                arrs[k][1] * self._order_df.loc[k, :][0], index=arrs[k][0], name=k
            )
            for k, v in arrs.items()
        ]
        self._recommender_df = pd.concat(products).sort_values(ascending=False)

    def _create_recommendation_dict(self, number_options: int):
        """get recommended products as dict to be serialized"""
        return self._recommender_df.round(2).head(number_options).to_dict()

    def _remove_already_bought(self):
        """ avoid recommending already bought products """
        self._recommender_df = self._recommender_df.drop(
            self._order_df.index, axis=0, errors="ignore"
        )

    def _remove_duplicates(self):
        """ group by the dataframes index """
        self._recommender_df = (
            self._recommender_df.groupby(level=0).sum().sort_values(ascending=False)
        )

    def get_recommendation(self, number_options: int):
        """process the manipulations and recommendation retrival"""

        self._set_recommender_df()
        self._remove_already_bought()
        self._remove_duplicates()

        return self._create_recommendation_dict(number_options=number_options)

    def set_user_recommendation(self, number_options: int):
        """ set recommendations to the associated user obejct"""
        self._user.set_recommendations(self.get_recommendation(number_options))
