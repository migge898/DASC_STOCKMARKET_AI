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

figy = px.line(x=df_result["ds"], y=df_result["yearly"])


# Set the axis labels
figy.update_layout(xaxis_title="date", yaxis_title="predicted values", title="Yearly")

app.layout = html.Div(
    children=[
        html.H2("DASC Stockmarket AI"),
        dcc.Dropdown(id="symbol-dropdown", options=symbol_options, value=symbols[0]),
        html.Div(id="stock_header"),
        # html.H1(f'{stock_names.get(symbol)} Stocks'),
        html.Div([html.H4("Stock History"), dcc.Graph(id="stock_graph", figure=fig)]),
        html.Div(
            [
                html.H4("Prediction"),
                dcc.Graph(id="stock_graph_prediction", figure=fig1),
                dcc.Graph(id="weekly_prediction", figure=figw),
                dcc.Graph(id="yearly_prediction", figure=figy),
            ]
        ),
    ]
)


# Define the callback to update the graph based on the dropdown selection


# Define the callback to update the graph based on the dropdown selection
@app.callback(
    [
        Output("stock_graph", "figure"),
        Output("stock_graph_prediction", "figure"),
        Output("weekly_prediction", "figure"),
        Output("yearly_prediction", "figure"),
        [Output("stock_header", "children")],
    ],
    [Input("symbol-dropdown", "value")],
)
def update_graph(selected_symbol):
    df_selected = pd.read_parquet(
        "..\.." / cleaned_data_path / f"{selected_symbol}.parquet"
    )

    fig_stocks = px.line(
        df_selected,
        x=df_selected.index,
        y="adjusted_close",
        labels={"index": "date", "adjusted_close": "adjusted close values"},
    )

    df_result = pd.read_csv(
        "..\.." / result_data_path / f"{selected_symbol}_prediction.csv"
    )
    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(x=df_result["ds"], y=df_result["yhat"], name="predicted value")
    )
    actual = df_selected.loc[df_selected.index.isin(df_result["ds"])]
    fig1.add_trace(
        go.Scatter(
            x=df_result["ds"],
            y=actual["adjusted_close"],
            name="actual adjusted close value",
            line_color="indigo",
        )
    )
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
    fig1.update_layout(
        xaxis_title="date", yaxis_title="predicted weekly values", title="Prediction"
    )

    figw = px.line(x=df_result["ds"], y=df_result["weekly"])
    figw.update_layout(
        xaxis_title="date", yaxis_title="predicted values", title="Weekly"
    )

    figy = px.line(x=df_result["ds"], y=df_result["yearly"])

    figy.update_layout(
        xaxis_title="date", yaxis_title="predicted values", title="Yearly"
    )

    return (
        fig_stocks,
        fig1,
        figw,
        figy,
        [html.H1(f"{stock_names.get(selected_symbol)} Stocks")],
    )


if __name__ == "__main__":
    app.run_server(debug=True)
