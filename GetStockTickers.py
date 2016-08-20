from csv import reader
from os import path

DIRNAME, _ = path.split(path.abspath(__file__))
FILES = ["amex.txt", "nasdaq.txt", "nyse.txt"]


def get_all_tickers():
    all_tickers = []
    for f in _get_file_path_list():
        tickers = _get_tickers_from_file(f)
        all_tickers += tickers
    return _filter_all_tickers(all_tickers)


def _get_file_path_list():
    paths = []
    full_path = path.join(DIRNAME, 'tickers')
    for f in FILES:
        paths.append(path.join(full_path, f))
    return paths


def _get_tickers_from_file(p):
    ticker_list = []
    with open(p, 'r') as csvfile:
        ticker_reader = reader(csvfile)
        for row in ticker_reader:
            if row[0] != 'Symbol':
                ticker_list.append(row[0].strip())
    return ticker_list


def _filter_all_tickers(all_tickers):
    filtered_list = []
    for ticker in all_tickers:
        if '^' not in ticker and '.' not in ticker and '$' not in ticker:
            filtered_list.append(ticker)
    filtered_list.sort()
    return filtered_list