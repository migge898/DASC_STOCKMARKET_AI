import requests
import csv
import os
import pandas as pd

from dasai.helpers import *

from dasai.stocks import my_key

no_articles_msg = (
    "{'Information': 'No articles found. "
    "Please adjust the time range or refer to the API documentation "
    "https://www.alphavantage.co/documentation#newsapi and try again.'}"
)

limit_reached_msg = (
    "{'Note': 'Thank you for using Alpha Vantage! "
    "Our standard API call frequency is 5 calls per minute and 500 calls"
    " per day. Please visit https://www.alphavantage.co/premium/ if you "
    "would like to target a higher API call frequency.'}"
)


def download_and_save_stock_data(symbol, overwrite=False):
    """
    Download stock data from Alpha Vantage and save it to a CSV file.

    :param symbol: the stock symbol
    :type symbol: str
    :param overwrite: if True, overwrite existing file
    :type overwrite: bool

    """
    url = (
        f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}"
        f"&datatype=csv&outputsize=full&apikey={my_key}"
    )
    # url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo"
    response = requests.get(url)

    if response.status_code == 200:
        # Get the CSV data from the response
        csv_data = response.text

        if csv_data == no_articles_msg or csv_data == limit_reached_msg:
            print(f"Error: {csv_data}")
            return
        else:
            # Write the CSV data to a file
            filepath = get_raw_data_path() / f"{symbol}.csv"

            # if file exists and overwrite is False, create a new file with a number

            if not overwrite:
                i = 1
                while os.path.exists(filepath):
                    filepath = get_raw_data_path() / f"{symbol}_{i}.csv"
                    i += 1

            with open(filepath, "w", newline="") as file:
                writer = csv.writer(file)
                reader = csv.reader(csv_data.splitlines())
                for row in reader:
                    writer.writerow(row)

            print("CSV file saved.")
    else:
        print("Error: Request failed with status code", response.status_code)


def convert_to_cleaned_data(input_file: str, output_file: str):
    """
    Convert the raw data to a cleaned data format.

    :param input_file: path to the raw data
    :type input_file: str
    :param output_file: path to the cleaned data
    :type output_file: str
    :return: cleaned data
    :rtype: pd.DataFrame
    """

    df = pd.read_csv(input_file)
    expected_columns = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "adjusted_close",
        "volume",
        "dividend_amount",
        "split_coefficient",
    ]
    assert all(
        column in df.columns for column in expected_columns
    ), f"Expected columns {expected_columns}, but got {df.columns.tolist()} instead."

    df = df.rename(columns={"timestamp": "date"})
    # timestamp column as timestamp and index
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    # get data from last 5 years
    five_years_ago = pd.Timestamp.today() - pd.Timedelta(days=365 * 5)
    df = df[df.index >= five_years_ago]

    # drop all columns except for adjusted_close
    df_adjusted_close = df[["adjusted_close"]]

    df_adjusted_close.to_parquet(output_file)

    return df
