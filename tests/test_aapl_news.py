import pandas as pd

from dasai.helpers import get_raw_data_path


def test_df_shape():
    raw_data_path = get_raw_data_path()
    df = pd.read_json(raw_data_path / "aapl_news.json")
    assert df.shape == (2000, 13)


def test_columns():
    raw_data_path = get_raw_data_path()
    df = pd.read_json(raw_data_path / "aapl_news.json")
    assert set(df.columns) == {
        "title",
        "url",
        "time_published",
        "authors",
        "summary",
        "banner_image",
        "source",
        "category_within_source",
        "source_domain",
        "topics",
        "overall_sentiment_score",
        "overall_sentiment_label",
        "ticker_sentiment",
    }
