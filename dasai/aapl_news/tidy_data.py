import pandas as pd

from dasai.helpers import get_raw_data_path
from dasai.helpers import get_tidy_data_path


def load_apple_news():
    """
    Loads the apple news from the .json file
    :return: Dataframe with raw news
    """
    raw_data_path = get_raw_data_path()
    return pd.read_json(raw_data_path / "aapl_news.json")


def transform_date(df: pd.DataFrame):
    """
    Transform the custom date-format-string to a real datetime
    :param df: Dataframe for which the column should be transformed
    :type df: pandas.Dataframe
    :return: Dataframe with transformed datetime column
    """
    df["time_published"] = pd.to_datetime(df["time_published"], format="%Y%m%dT%H%M%S")
    return df


def remove_useless_columns(df: pd.DataFrame):
    """
    Keep only relevant columns for analysis
    :param df: Dataframe to remove columns from
    :type df: pandas.Dataframe
    :return: reduced Dataframe
    """
    return df[
        [
            "time_published",
            "source",
            "category_within_source",
            "overall_sentiment_score",
            "ticker_sentiment",
        ]
    ]


# Remove all ticker details despite the relevant AAPL one
# (within the column named ticker_sentiment)


def flatten_nested_json_df(df):
    """
    Search for columns to explode/flatten recursively
    :param df: Dataframe to flatten
    :type df: pandas.Dataframe
    :return: Flattened and exploded dataframe
    """
    df = df.reset_index()

    print(f"original shape: {df.shape}")
    print(f"original columns: {df.columns}")

    # search for columns to explode/flatten
    s = (df.applymap(type) == list).all()
    list_columns = s[s].index.tolist()

    s = (df.applymap(type) == dict).all()
    dict_columns = s[s].index.tolist()

    print(f"lists: {list_columns}, dicts: {dict_columns}")
    while len(list_columns) > 0 or len(dict_columns) > 0:
        new_columns = []

        for col in dict_columns:
            print(f"flattening: {col}")
            # explode dictionaries horizontally, adding new columns
            horiz_exploded = pd.json_normalize(df[col]).add_prefix(f"{col}.")
            horiz_exploded.index = df.index
            df = pd.concat([df, horiz_exploded], axis=1).drop(columns=[col])
            new_columns.extend(horiz_exploded.columns)  # inplace

        for col in list_columns:
            print(f"exploding: {col}")
            # explode lists vertically, adding new columns
            df = df.drop(columns=[col]).join(df[col].explode().to_frame())
            new_columns.append(col)

        # check if there are still dict o list fields to flatten
        s = (df[new_columns].applymap(type) == list).all()
        list_columns = s[s].index.tolist()

        s = (df[new_columns].applymap(type) == dict).all()
        dict_columns = s[s].index.tolist()

        print(f"lists: {list_columns}, dicts: {dict_columns}")

    print(f"final shape: {df.shape}")
    print(f"final columns: {df.columns}")
    return df


def flatten_ticket_sentiment(df: pd.DataFrame):
    """
    Flatten/explode the json list ticker_sentiment
    :param df: Dataframe to flatten
    :type df: pandas.Dataframe
    :return: Flat and exploded Dataframe
    """
    df = flatten_nested_json_df(df)
    df = df.set_index("index")

    return df


def tidy_data(df: pd.DataFrame):
    """
    A function to tidy the raw apple news data up
    (keep only relevant ticker, remove useless column 'ticker',
    rename some columns and set correct datatypes)
    :param df: Dataframe to clean
    :type df: pandas.Dataframe
    :return: A clean and reduced version of the input Dataframe
    """
    # keep only the entries with the relevant ticker
    df = df.query('`ticker_sentiment.ticker` == "AAPL"')

    # remove ticker column (it contains "AAPL" for every entry)
    df = df.drop(
        ["ticker_sentiment.ticker", "ticker_sentiment.ticker_sentiment_label"], axis=1
    )

    # rename columns
    df = df.rename(
        columns={
            "category_within_source": "category",
            "ticker_sentiment.relevance_score": "relevance_score_aapl",
            "ticker_sentiment.ticker_sentiment_score": "sentiment_score_aapl",
        }
    )

    # set correct datatypes
    df["category"] = df["category"].astype("category")
    df["relevance_score_aapl"] = df["relevance_score_aapl"].astype("float64")
    df["sentiment_score_aapl"] = df["sentiment_score_aapl"].astype("float64")

    return df


def save_dataframe(df: pd.DataFrame):
    """
    Saves the specified Dataframe as a .parquet file
    :param df: The Dataframe to save
    :type df: pandas.Dataframe
    :return: None
    """
    tidy_data_path = get_tidy_data_path()
    tidy_data_path.mkdir(parents=True, exist_ok=True)
    df.to_parquet(tidy_data_path / "aapl_news.parquet")
    print(f"Dataframe has been saved at {tidy_data_path / 'aapl_news.parquet'}")


def tidy_and_save_news():
    """
    Loads the raw .json file, create tidy data from it and save this as a .parquet file
    :return: None
    """
    df = load_apple_news()
    df = transform_date(df)
    df = remove_useless_columns(df)
    df = flatten_ticket_sentiment(df)
    df = tidy_data(df)
    save_dataframe(df)


if __name__ == "__main__":
    tidy_and_save_news()
