import requests
import csv
import os

from dasai.helpers import get_raw_data_path

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
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}" \
          f"&datatype=csv&outputsize=full&apikey={my_key}"
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
            filepath = get_raw_data_path() / f'{symbol}.csv'

            # if file exists and overwrite is False, create a new file with a number

            if not overwrite:
                i = 1
                while os.path.exists(filepath):
                    filepath = get_raw_data_path() / f'{symbol}_{i}.csv'
                    i += 1

            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                reader = csv.reader(csv_data.splitlines())
                for row in reader:
                    writer.writerow(row)

            print('CSV file saved.')
    else:
        print('Error: Request failed with status code', response.status_code)
