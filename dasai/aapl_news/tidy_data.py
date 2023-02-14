import pandas as pd

from dasai.helpers import get_raw_data_path
from dasai.helpers import get_tidy_data_path
print("start")
# load data from json file
raw_data_path = get_raw_data_path()
df = pd.read_json(raw_data_path / 'aapl_news.json')
print("after read")

# Transform the custom date-format-string to a real date
df['time_published'] = \
    pd.to_datetime(df['time_published'], format='%Y%m%dT%H%M%S')

# Keep only interesting columns
df = \
    df[['time_published', 'source',
        'category_within_source', 'overall_sentiment_score',
        'ticker_sentiment']]


# Remove all ticker details despite the relevant AAPL one
# (within the column named ticker_sentiment)

def flatten_nested_json_df(df):
    """
    Search for columns to explode/flatten recursively
    :param df: Dataframe to flatten
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
            horiz_exploded = pd.json_normalize(df[col]).add_prefix(f'{col}.')
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


# first flatten the json list ticker_sentiment
df = flatten_nested_json_df(df)
df = df.set_index('index')

# then keep only the entries with the relevant ticker
df = df.query('`ticker_sentiment.ticker` == "AAPL"')

# remove ticker column (it contains "AAPL" for every entry)
df = df.drop(['ticker_sentiment.ticker',
              'ticker_sentiment.ticker_sentiment_label'], axis=1)

# rename columns
df = df.rename(columns={
    'category_within_source': 'category',
    'ticker_sentiment.relevance_score': 'relevance_score_aapl',
    'ticker_sentiment.ticker_sentiment_score': 'sentiment_score_aapl',
})

# set correct datatypes
df['category'] = df['category'].astype('category')
df['relevance_score_aapl'] = df['relevance_score_aapl'].astype('float64')
df['sentiment_score_aapl'] = df['sentiment_score_aapl'].astype('float64')

# save tidy data in better format
tidy_data_path = get_tidy_data_path()
tidy_data_path.mkdir(parents=True, exist_ok=True)
df.to_parquet(tidy_data_path / 'aapl_news.parquet')
print("Dataframe has been saved")
