from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
from dasai.helpers import get_cleaned_data_path, get_tidy_data_path


app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])



# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
cleaned_data_path = get_cleaned_data_path()
tidy_data_path = get_tidy_data_path()


symbols =['AAPL', 'NFLX', 'KO', 'IBM', 'MSFT']
symbol = symbols[0]

stock_names= {'AAPL': 'Apple' , 'NFLX': 'Netflix', 'KO': 'Coca Cola', 'IBM': 'IBM', 'MSFT': 'Microsoft'}

df_stocks = pd.read_parquet('..\..' / cleaned_data_path / f'{symbol}.parquet')
df_news = pd.read_parquet('..\..' / tidy_data_path / f'{symbol.lower()}_news_dense.parquet')

# Define the dropdown options
symbol_options = [{'label': symbol, 'value': symbol} for symbol in symbols]
dcc.Dropdown(
    id='symbol-dropdown',
    options=symbol_options,
    value=symbols[0]
),

# print(df_stocks.describe(include='all') )
# print(df_news.columns)
df_stocks.reset_index()

fig = px.line(
    df_stocks,
    x=df_stocks.index,
    y='adjusted_close',
    labels={'index': 'date', 'adjusted_close' : 'adjusted close values'}

)

fig1 = px.line(
    df_stocks.head(10),
    x=df_stocks.head(10).index,
    y='adjusted_close',
    labels={'x': 'date', 'adjusted_close' : 'adjusted close values'}

)

# Define the dropdown options
options = [{'label': i, 'value': i} for i in df_news['source'].unique()]

fig2 = px.scatter(
    df_news,
    x='time_published',
    y=f'sentiment_score_{symbol.lower()}',
    color='source',
    size=f'relevance_score_{symbol.lower()}',
    color_continuous_scale='ice',
    opacity=0.6,
    labels={'x': 'date', 'y' : 'sentiment score'}
)

app.layout = html.Div(children=[
    html.H2('DASC Stockmarket AI'),
    dcc.Dropdown(
        id='symbol-dropdown',
        options=symbol_options,
        value=symbols[0]
    ),

    html.H1(f'{stock_names.get(symbol)} Stocks'),

    html.Div([
        html.H4('Stock History'),
        dcc.Graph(
            id='stock_graph',
            figure=fig
        )
    ]),
    html.Div([
        html.H4('Prediction'),
        dcc.Graph(
            id='stock_graph_prediction',
            figure=fig1
        )
    ]),

    html.Div([
        html.H4('Sentiment Score by News'),
        html.P('News Source:'),
        dcc.Dropdown(id='source-dropdown', options=options, value='Forbes'),
        dcc.Graph(
            id='news_graph',
            figure=fig2
        )
    ])
])



# Define the callback to update the graph based on the dropdown selection

@app.callback(
    [
        Output('stock_graph', 'figure'),
        Output('news_graph', 'figure')
    ],
    [
        Input('symbol-dropdown', 'value'),
        Input('source-dropdown', 'value')
    ]

)
def update_graph(symbol, selected_news_source):
    df_stocks = pd.read_parquet('..\..' / cleaned_data_path / f'{symbol}.parquet')
    df_news = pd.read_parquet('..\..' / tidy_data_path / f'{symbol.lower()}_news_dense.parquet')

    filtered_df = df_news[df_news['source'] == selected_news_source]



    fig_stocks = px.line(
        df_stocks,
        x=df_stocks.index,
        y='adjusted_close'
    )

    options = [{'label': i, 'value': i} for i in df_news['source'].unique()]

    fig_news = px.scatter(
        filtered_df,
        x='time_published',
        y=f'sentiment_score_{symbol.lower()}',
        color='source',
        size=f'relevance_score_{symbol.lower()}',
        color_continuous_scale='ice',
        opacity=0.6
    )


    return fig_stocks, fig_news

if __name__ == '__main__':
    app.run_server(debug=True)
