from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dasai.helpers import (
    get_cleaned_data_path,
    get_tidy_data_path,
    get_result_data_path,
)

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
cleaned_data_path = get_cleaned_data_path()
tidy_data_path = get_tidy_data_path()
result_data_path = get_result_data_path()

symbols = ["AAPL", "NFLX", "KO", "IBM", "MSFT"]
symbol = symbols[0]

stock_names = {
    "AAPL": "Apple",
    "NFLX": "Netflix",
    "KO": "Coca Cola",
    "IBM": "IBM",
    "MSFT": "Microsoft",
}

df_stocks = pd.read_parquet("..\.." / cleaned_data_path / f"{symbol}.parquet")
if symbol == "AAPL":
    df_news = pd.read_parquet(
        "..\.." / tidy_data_path / f"{symbol.lower()}_news_dense.parquet"
    )
df_result = pd.read_csv("..\.." / result_data_path / f"{symbol}_prediction.csv")

# print(df_result)

# Define the dropdown options
symbol_options = [{"label": symbol, "value": symbol} for symbol in symbols]
dcc.Dropdown(id="symbol-dropdown", options=symbol_options, value=symbols[0]),

# print(df_stocks.describe(include='all') )
# print(df_news.columns)
df_stocks.reset_index()

fig = px.line(
    df_stocks,
    x=df_stocks.index,
    y="adjusted_close",
    labels={"index": "date", "adjusted_close": "adjusted close values"},
)

fig1 = go.Figure()

# Add the line trace for yhat
fig1.add_trace(
    go.Scatter(x=df_result["ds"], y=df_result["yhat"], name="predicted value")
)

actual = df_stocks.loc[df_stocks.index.isin(df_result["ds"])]


fig1.add_trace(
    go.Scatter(
        x=df_result["ds"],
        y=actual["adjusted_close"],
        name="actual adjusted close value",
        line_color="indigo",
    )
)


# Add the fill trace between yhat_lower and yhat_upper
fig1.add_trace(
    go.Scatter(
        x=df_result["ds"],
        y=df_result["yhat_upper"],
        fill=None,
        mode="lines",
        line_color="rgba(0,0,0,0)",
        showlegend=False,
    )
)

fig1.add_trace(
    go.Scatter(
        x=df_result["ds"],
        y=df_result["yhat_lower"],
        fill="tonexty",
        mode="lines",
        line_color="rgba(0,0,0,0)",
        name="confidence interval",
    )
)


# Set the axis labels
fig1.update_layout(
    xaxis_title="date", yaxis_title="predicted weekly values", title="Prediction"
)

figw = px.line(x=df_result["ds"], y=df_result["weekly"])


# Set the axis labels
figw.update_layout(xaxis_title="date", yaxis_title="predicted values", title="Weekly")
# Define the dropdown options
options = [{"label": i, "value": i} for i in df_news["source"].unique()]

fig2 = px.scatter(
    df_news,
    x="time_published",
    y=f"sentiment_score_{symbol.lower()}",
    color="source",
    size=f"relevance_score_{symbol.lower()}",
    color_continuous_scale="ice",
    opacity=0.6,
    labels={"x": "date", "y": "sentiment score"},
)

app.layout = html.Div(
    children=[
        html.H2("DASC Stockmarket AI"),
        dcc.Dropdown(id="symbol-dropdown", options=symbol_options, value=symbols[0]),
        html.H1(f"{stock_names.get(symbol)} Stocks"),
        html.Div([html.H4("Stock History"), dcc.Graph(id="stock_graph", figure=fig)]),
        html.Div(
            [
                html.H4("Prediction"),
                dcc.Graph(id="stock_graph_prediction", figure=fig1),
                dcc.Graph(id="weekly_prediction", figure=figw),
            ]
        ),
        html.Div(
            [
                html.H4("Sentiment Score by News"),
                html.P("News Source:"),
                dcc.Dropdown(id="source-dropdown", options=options, value="Forbes"),
                dcc.Graph(id="news_graph", figure=fig2),
            ]
        ),
    ]
)


# Define the callback to update the graph based on the dropdown selection


@app.callback(
    [Output("stock_graph", "figure"), Output("news_graph", "figure")],
    [Input("symbol-dropdown", "value"), Input("source-dropdown", "value")],
)
def update_graph(symbol, selected_news_source):
    df_stocks = pd.read_parquet("..\.." / cleaned_data_path / f"{symbol}.parquet")
    if symbol == "AAPL":
        df_news = pd.read_parquet(
            "..\.." / tidy_data_path / f"{symbol.lower()}_news_dense.parquet"
        )

        filtered_df = df_news[df_news["source"] == selected_news_source]

        # options = [{'label': i, 'value': i} for i in df_news['source'].unique()]

        fig_news = px.scatter(
            filtered_df,
            x="time_published",
            y=f"sentiment_score_{symbol.lower()}",
            color="source",
            size=f"relevance_score_{symbol.lower()}",
            opacity=0.6,
        )
    fig_stocks = px.line(
        df_stocks,
        x=df_stocks.index,
        y="adjusted_close",
        labels={"index": "date", "adjusted_close": "adjusted close values"},
    )
    if symbol == "AAPL":
        return fig_stocks, fig_news
    return fig_stocks


if __name__ == "__main__":
    app.run_server(debug=True)
