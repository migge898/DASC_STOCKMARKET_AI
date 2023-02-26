from typing import Tuple

import pandas as pd
from pandas import DataFrame

from dasai.helpers import *
from prophet import Prophet


def predict_stock_price(stock_df: pd.DataFrame, output_file: str = None,
                        train_quantile: float = 0.8) -> Tuple[Prophet, DataFrame]:
    """
    Predict stock price using Prophet and saving the results to a csv file if output_file is specified.
    :param stock_df: Dataframe containing stock data
    :type stock_df: pandas.Dataframe
    :param output_file: Path to output file
    :type output_file: str
    :param train_quantile: Quantile for splitting training data
    :type train_quantile: float
    :return: Prophet model and forecast
    :rtype: Tuple[Prophet, pandas.Dataframe]
    """
    # assert that stock_df has columns 'date' and 'adjusted_close'
    assert all(column in stock_df.reset_index().columns for column in
               ['date',
                'adjusted_close']), f"Expected columns ['date', 'adjusted_close']," \
                                    f" but got {stock_df.columns.tolist()} instead."

    df_prophet = stock_df.reset_index().rename(columns={'date': 'ds', 'adjusted_close': 'y'})

    date_train = df_prophet['ds'].quantile(train_quantile)
    df_train = df_prophet[df_prophet['ds'] < date_train]

    df_test = df_prophet[df_prophet['ds'] >= date_train]

    m = Prophet(
        seasonality_prior_scale=0.1,
    )

    m.fit(df_train)

    future_test = df_test[['ds']]

    forecast_test = m.predict(future_test)

    if output_file:
        forecast_test.to_csv(output_file)

    return m, forecast_test
