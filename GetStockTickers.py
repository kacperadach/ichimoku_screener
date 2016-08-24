from re import findall
from csv import reader
from os import path
from urllib2 import Request, urlopen, URLError
from ftplib import FTP

from Logger import get_logger

logger = get_logger()
DIRNAME, _ = path.split(path.abspath(__file__))
FILES = ["amex.txt", "nasdaq.txt", "nyse.txt"]
BASE_PATH = path.dirname(path.abspath(__file__))

def get_all_tickers_from_ftp():
    _write_all_tickers_from_ftp()
    ticker_file = open(path.join(BASE_PATH, 'tickers/all_tickers.txt'), 'r')
    all_tickers = []
    for line in ticker_file:
        ticker = line.split('|')[0]
        if ticker.upper() != 'SYMBOL':
            all_tickers.append(ticker)
    logger.info("Found {} tickers using ftp".format(len(all_tickers)))
    return _filter_all_tickers(all_tickers)


def _write_all_tickers_from_ftp():
    try:
        ticker_file = open(path.join(BASE_PATH, 'tickers/all_tickers.txt'), 'wb')
        ftp = FTP('ftp.nasdaqtrader.com')
        ftp.login()
        ftp.cwd('SymbolDirectory')
        ftp.retrbinary('RETR {}'.format('nasdaqlisted.txt'), ticker_file.write)
        ftp.retrbinary('RETR {}'.format('otherlisted.txt'), ticker_file.write)
    except:
        logger.error("Error retrieving tickers from NASDAQ ftp")

def get_all_tickers_from_api():
    all_tickers = []
    for exchange in ('nasdaq', 'nyse', 'amex'):
        request = Request(get_api_url(exchange))
        try:
            response = urlopen(request)
            tickers = response.read()
            _write_tickers_to_file(exchange, tickers)
            ticker_list = tickers.split("\n")
            for ticker in ticker_list:
                try:
                    ticker_string = findall('"([^"]*)"', ticker)[0]
                    if not ticker_string.lower() == 'symbol':
                        all_tickers.append(ticker_string)
                except IndexError:
                    continue
        except URLError:
            logger.error("Error retrieving tickers from API")
    logger.info("Found {} tickers using api".format(len(all_tickers)))
    return _filter_all_tickers(all_tickers)

def _write_tickers_to_file(exchange, file_data_string):
   file_path = path.join(path.join(path.dirname(path.abspath(__file__)), 'tickers'), (exchange + '.txt'))
   with open(file_path, 'w') as f:
       f.write(file_data_string)

def get_api_url(exchange):
    return 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange={}&render=download'.format(exchange)


def get_all_tickers_from_file():
    all_tickers = []
    for f in _get_file_path_list():
        tickers = _get_tickers_from_file(f)
        all_tickers += tickers
    logger.info("Found {} tickers using static file".format(len(all_tickers)))
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