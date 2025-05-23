import os
import time

import pandas as pd
import requests
from dotenv import load_dotenv

from dasai.helpers import get_raw_data_path

# get the alphavantage API key
load_dotenv()
my_key = os.getenv("alphavantage_key")

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


def generate_time_limit_strings_2022():
    """
    Generate date strings in a specific format

    :return: time_limits contains dates with a 5-day gap for all months of 2022
    """
    # skip january and february
    # days_of_month = [31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    time_limits = []
    for i in range(3, 13):
        month = f"{i}" if i > 9 else f"0{i}"  # two-digit month
        time_limits.append(f"2022{month}01T0101")
        time_limits.append(f"2022{month}05T0101")
        time_limits.append(f"2022{month}10T0101")
        time_limits.append(f"2022{month}15T0101")
        time_limits.append(f"2022{month}20T0101")
        time_limits.append(f"2022{month}25T0101")
    return time_limits


def get_news_by_month(time_from: object, time_to: object):
    """
    Helper function to get the most relevant apple news of 2022 by publishing month
    This function returns more evenly distributed and more dense data

    :param time_from: Start time of the news you want
    :type time_from: string
    :param time_to: Max. publishing date of the news you want
    :type time_to: string
    :return: Max. 200 most relevant apple news of specified timeframe
    """
    tickers = "AAPL"
    sort = "RELEVANCE"
    limit = 200

    url = (
        "https://www.alphavantage.co/query?"
        "function=NEWS_SENTIMENT&"
        f"tickers={tickers}&"
        f"time_from={time_from}&"
        f"time_to={time_to}&"
        f"sort={sort}&"
        f"limit={limit}&"
        f"apikey={my_key}"
    )
    r = requests.get(url)
    data = r.json()
    if str(data) == no_articles_msg:
        return False, pd.DataFrame()
    if str(data) == limit_reached_msg:
        raise Exception("API token limit exceeded")
    return True, pd.DataFrame(data["feed"])


def get_aapl_news_2022():
    """
    Gets the apple news for each month of 2022 and concatenate to one Dataframe
    News are requested in 5-day timeframes to ensure an evenly distributed newsfeed

    :return: The concatenated Dataframe with the most relevant Apple-news of 2022 (more evenly distributed)
    """
    retry_counter = 0
    max_retries = 3
    time_limits = generate_time_limit_strings_2022()

    df = pd.DataFrame()
    i = 0
    # for all timeframes
    while i <= len(time_limits) - 2 and retry_counter < max_retries:
        time_from = time_limits[i]
        time_to = time_limits[i + 1]
        try:
            is_data_found, df_month = get_news_by_month(time_from, time_to)
            if is_data_found:
                # reset retry counter
                print(f"{time_from}-{time_to}: Data has been successfully fetched")
                retry_counter = 0
                df = pd.concat([df, df_month])
            else:
                print(f"{time_from}-{time_to}: No data has been found")
            i += 1
        except Exception as e:
            if str(e) == "API token limit exceeded":
                retry_counter += 1
                print(
                    f"{time_from}-{time_to}: API call limit reached. "
                    f"Waiting for 65 seconds before retrying "
                    f"(retry={retry_counter}) ..."
                )
                time.sleep(65)
            else:
                print(
                    f"{time_from}-{time_to}: Exception occurred. Timeframe will be skipped"
                )
                i += 1
    return df


def adjust_dataframe(df: pd.DataFrame):
    """
    This function cleans leftovers created by the concatenations

    :param df: Dataframe to adjust
    :type df: pandas.Dataframe
    :return: Adjusted Dataframe
    """
    # reset index for unique indexes
    df = df.reset_index()

    # drop index column inherited from monthly dataframes
    df = df.drop(["index"], axis=1)

    return df


def save_dataframe_to_file(df: pd.DataFrame):
    """
    Save the Dataframe to a json file

    :param df: Dataframe to save
    :type df: pandas.Dataframe
    :return: None
    """
    # safe the json object to a file for easier access
    raw_data_path = get_raw_data_path()
    raw_data_path.mkdir(parents=True, exist_ok=True)

    df.to_json(raw_data_path / "aapl_news_dense.json")


def load_and_save_news_2022():
    """
    This function will get the news, adjust them and then save them to a .json file

    :return: None
    """
    df = get_aapl_news_2022()
    df = adjust_dataframe(df)
    save_dataframe_to_file(df)


if __name__ == "__main__":
    load_and_save_news_2022()
