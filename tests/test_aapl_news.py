import pandas as pd

from dasai.helpers import get_raw_data_path


def test_df_shape():
    raw_data_path = get_raw_data_path()
    df = pd.read_json(raw_data_path / 'aapl_news.json')
    assert df.shape == (2000, 6)


def test_columns():
    raw_data_path = get_raw_data_path()
    df = pd.read_json(raw_data_path / 'aapl_news.json')
    assert df.columns == ['time_published', 'source', 'category', 'overall_sentiment_score',
                          'relevance_score_aapl', 'sentiment_score_aapl']
