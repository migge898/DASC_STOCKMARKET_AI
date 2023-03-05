# DASAI (Data Science Stockmarket AI)
![App Status](https://github.com/migge898/DASC_STOCKMARKET_AI/actions/workflows/python-app.yml/badge.svg?branch=development)
![Linter Status](https://github.com/migge898/DASC_STOCKMARKET_AI/actions/workflows/lint.yml/badge.svg?branch=development)

## Description
Group-Project for module Data-Science at [TH Bingen](https://www.th-bingen.de/).

This project is our first attempt to create a stock market prediction model using Facebook's Prophet library.
We had two approaches to the problem:
1. Focus on Apple: We used the stock price of Apple and enriched it with news data
2. General focus: We used pure stock data of Apple, Microsoft, Coca-Cola, IBM, Netflix to predict the stock price respectively

Due to time limitations, our team has focused on creating a more straightforward prototype for predicting stock data,
as well as setting up a streamlined CI/CD pipeline and a visually appealing dashboard.  
While we recognize that there is always room for improvement, we believe that these efforts will lay the groundwork for future automation
and expansion of our project.  
By laying a strong foundation, we can ensure that our work is scalable and sustainable for the long-term.

## Documentation
The public [documentation](https://migge898.github.io/DASC_STOCKMARKET_AI/) contains the main modules and functions of the project.
It is hosted on GitHub Pages and is automatically updated after every push to a branch.

## Installation and Setup
`dasai` requires Python 3.8 or higher (3.10 recommended). It is recommended to use a virtual environment. 

Clone the repository and install the dependencies:
```bash
cd DASC_STOCKMARKET_AI
pip install -r requirements.txt
```

Also, you need an API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key) to load the data. After you have received the key, you must create a file called `.env` in the root directory of the project and add the following line:
``` bash
ALPHAVENTAGE_API_KEY=<your_api_key>
```

### CI/CD
We use GitHub Actions to run our CI/CD pipeline. At the moment, we have three [workflows](https://github.com/migge898/DASC_STOCKMARKET_AI/tree/development/.github/workflows):
1. `python-app.yml`: Builds and tests the project on every push or pull request to the `development` or `main` branch.
2. `lint.yml`: Runs the linter on every push or pull request to the `development` or `main` branch and can reformat the code if necessary.
3. `sphinx.yml`: This workflow automatically builds the documentation every time a push is made to any branch and pushes it to the `gh-pages` branch.

## Usage
We have developed a set of [notebooks](https://github.com/migge898/DASC_STOCKMARKET_AI/tree/development/notebooks_public) that not only demonstrate the usage of our modules but also serve as a valuable resource for testing and tutorials.

## Results
Our results come in two flavors:
1. The notebooks: [Apple prediction with news](https://github.com/migge898/DASC_STOCKMARKET_AI/blob/development/notebooks_public/Apple_News.ipynb) and [General prediction](https://github.com/migge898/DASC_STOCKMARKET_AI/blob/development/notebooks_public/Predictions.ipynb)
2. The [dashboard](https://github.com/migge898/DASC_STOCKMARKET_AI/blob/development/dasai/dashboard/dashboard.py)

## License
[MIT](https://choosealicense.com/licenses/mit/)