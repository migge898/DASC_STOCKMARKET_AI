from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from dasai.helpers import get_cleaned_data_path, get_tidy_data_path
import os

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
cleaned_data_path = get_cleaned_data_path()
tidy_data_path = get_tidy_data_path()
print(os.getcwd())

df_stocks = pd.read_parquet('..\..' / cleaned_data_path / 'AAPL.parquet')
df_news = pd.read_parquet('..\..' / tidy_data_path / f'aapl_news.parquet')

# print(df_stocks.describe(include='all') )
# print(df_news.columns)
df_stocks.reset_index()

fig = px.line(
    df_stocks,
    x=df_stocks.index,
    y='adjusted_close',

)

# Define the dropdown options
options = [{'label': i, 'value': i} for i in df_news['source'].unique()]
fig2 = px.scatter(
    df_news,
    x='time_published',
    y='sentiment_score_aapl',
    color='source',
    size='relevance_score_aapl',
    color_continuous_scale='ice',
    opacity=0.4
)

app.layout = html.Div(children=[
    html.H2('DASC Stockmarket AI'),
    html.H4('Stock History'),
    dcc.Graph(
        id='stock_graph',
        figure=fig
    ),
    html.H4('Sentiment Score by News'),
    html.P('News Source:'),
    dcc.Dropdown(id='source-dropdown', options=options, value='Forbes'),
    dcc.Graph(
        id='news_graph',
        figure=fig2
    )
])


# Define the callback to update the graph based on the dropdown selection
@app.callback(
    Output('news_graph', 'figure'),
    [Input('source-dropdown', 'value')]
)
def update_graph(selected_news_source):
    filtered_df = df_news[df_news['source'] == selected_news_source]
    fig2 = px.scatter(filtered_df, x='time_published', y='sentiment_score_aapl', size='relevance_score_aapl')
    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)
