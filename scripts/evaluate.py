# %%
import pandas as pd
import numpy as np

from src.prepare import prep_data, create_sim_matrix
from src.user import User
from src.recommender import Recommender
from src.cache import CachedData


def split_data(df: pd.DataFrame, ith_perc: float, date_field: str):
    """ Split the DataFrame on the ith percentile of the Datefield """
    df[date_field] = pd.to_datetime(df[date_field], format="%m/%d/%Y %H:%M")
    threshhold = df[[date_field]].quantile(ith_perc, numeric_only=False)[0]
    return (
        df[df[date_field] <= threshhold],
        df[df[date_field] > threshhold],
    )


def train(
    df: pd.DataFrame, sim_measure: str, item_field: str = "Description", **kwargs
):
    """ train model by creating a similarity matrix """
    return create_sim_matrix(df, sim_measure, item_field, **kwargs)


def get_test_users(df_train: pd.DataFrame, df_test: pd.DataFrame, id_field: str):
    """ for the test, use only customers that appear in both"""
    return (
        df_train[df_train[id_field].isin(df_test[id_field])][id_field].dropna().unique()
    )


def extract_model_input(
    df_train: pd.DataFrame, user_id: int, item_field: str = "Description"
):
    """ model input must be a dictionary containing the past orders of the user"""
    order_df = df_train[df_train["CustomerID"] == user_id][[item_field, "InvoiceNo"]]
    return order_df.groupby(item_field)["InvoiceNo"].count().astype("float").to_dict()


def predict(user_id: int, orders: dict, sim_matrix: pd.DataFrame, number_options: int):
    """ input the model with given params and retrieve a product recommendation """
    data = CachedData(sim_matrix=sim_matrix)
    user = User(id=user_id, orders=orders)
    recommender = Recommender(data=data, user=user)
    return recommender.get_recommendation(number_options)


def test(user_id: int, df_test: pd.DataFrame, recommendations: dict):
    """ compare predicition to orders and calculate accuracy metrics"""
    y_true = np.array(
        df_test[df_test["CustomerID"] == user_id]["Description"], dtype="object"
    )
    y_pred = np.array(list(recommendations.keys()), dtype="object")
    return calc_precision(y_true, y_pred), calc_recall(y_true, y_pred)


def calc_precision(y_true: np.array, y_pred: np.array):
    return len(np.intersect1d(y_true, y_pred)) / len(y_pred)


def calc_recall(y_true: np.array, y_pred: np.array):
    return len(np.intersect1d(y_true, y_pred)) / len(y_true)


def calc_f_score(recall: float, precision: float):
    return 2 * precision * recall / (precision + recall)


# %%
# create similarity matrix from train data set and model input
# (train dataset because we give the past orders as input)


def pocess(similiarity_measure: str, number_options: int, min_orders: int, **kwargs):
    """
    run the evaluation process with different parameters
    :param similiarity_measure: string, one of 'correlation' or 'cosine'
    :param number_options: the number of recommended products to
    :param min_orders: only recommend if this minimum of past orders is provided
    """
    df_train, df_test = split_data(
        df=prep_data("../data/OnlineRetail.csv"), ith_perc=0.8, date_field="InvoiceDate"
    )
    sim_matrix = train(df_train, sim_measure=similiarity_measure, **kwargs)
    test_users = get_test_users(df_train, df_test, "CustomerID")
    results = []
    for test_user in test_users:
        test_user_orders = extract_model_input(df_train, user_id=test_user)
        if len(test_user_orders) >= min_orders:
            recommendations = predict(
                user_id=test_user,
                orders=test_user_orders,
                sim_matrix=sim_matrix,
                number_options=number_options,
            )
            if len(recommendations.keys()) > 0:
                results.append(test(test_user, df_test, recommendations))
    result_df = pd.DataFrame(columns=["precision", "recall"], data=results)
    avg_precision = result_df.precision.mean()
    avg_recall = result_df.recall.mean()
    print("\n")
    print(
        f"Model Parameters are similiarity_measure: {similiarity_measure}, "
        + f"number_options: {str(number_options)}, min_orders: {str(min_orders)}"
    )
    print("AVG: Precision is: " + str(round(avg_precision, 3)))
    print("AVG: Recall is: " + str(round(avg_recall, 3)))
    print("AVG: F-Score is: " + str(round(calc_f_score(avg_recall, avg_precision), 3)))
    print(f"Test results for {str(len(results))} predictions")


# %%

# this can take ver long!
measures = ["correlation", "cosine"]
numbers_options = [5, 10]
min_orders = [3, 6]
min_periods = [20, 40]
methods = ["pearson", "spearman"]
for measure in measures:
    for number_options in numbers_options:
        for min_order in min_orders:
            if measure == "correlation":
                for min_period in min_periods:
                    for mehtod in methods:
                        pocess(
                            measure,
                            number_options,
                            min_order,
                            min_periods=min_period,
                            method=mehtod,
                        )
            else:
                pocess(measure, number_options, min_order)
# %%
