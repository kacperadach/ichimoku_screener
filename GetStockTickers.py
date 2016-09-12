from re import findall
from csv import reader
from os import path
from urllib2 import Request, urlopen, URLError
from ftplib import FTP

from Logger import get_logger
from Constants import FILES, \
    SPECIFIC_PATH, \
    IGNORED_STRINGS, \
    FTP_ADDRESS, \
    FTP_CWD, \
    NASDAQ_FILE, \
    OTHER_FILE, \
    FTP_DELIMITER, \
    FILTERED_SYMBOLS, \
    EXCHANGES, \
    API_URL, \
    TICKERS_FOLDER

logger = get_logger()

DIRNAME, _ = path.split(path.abspath(__file__))
BASE_PATH = path.dirname(path.abspath(__file__))

def get_all_tickers_from_ftp(base=BASE_PATH, specific=SPECIFIC_PATH):
    _write_all_tickers_from_ftp(base, specific)
    all_tickers = _pull_all_tickers_from_file(base, specific)
    logger.info("Found {} tickers using ftp".format(len(all_tickers)))
    return _filter_all_tickers(all_tickers)

def _pull_all_tickers_from_file(base, specific):
    ticker_file = open(path.join(base, specific), 'r')
    all_tickers = []
    for line in ticker_file:
        if FTP_DELIMITER in line:
            ticker = line.split(FTP_DELIMITER)[0]
            if ticker.upper() not in IGNORED_STRINGS:
                all_tickers.append(ticker)
    return all_tickers

def _write_all_tickers_from_ftp(base, specific):
    try:
        ticker_file = open(path.join(base, specific), 'wb')
        ftp = FTP(FTP_ADDRESS)
        ftp.login()
        ftp.cwd(FTP_CWD)
        ftp.retrbinary('RETR {}'.format(NASDAQ_FILE), ticker_file.write)
        ftp.retrbinary('RETR {}'.format(OTHER_FILE), ticker_file.write)
    except:
        logger.error("Error retrieving tickers from NASDAQ ftp")

def get_all_tickers_from_api(file_path=None, exchanges=EXCHANGES):
    all_tickers = []
    for exchange in exchanges:
        try:
            tickers = get_api_response(exchange)
            _write_tickers_to_file(exchange, tickers, file_path)
            ticker_list = extract_tickers_from_api_response(tickers)
            all_tickers += ticker_list
        except URLError:
            logger.error("Error retrieving tickers from API")
    logger.info("Found {} tickers using api".format(len(all_tickers)))
    return _filter_all_tickers(map(lambda x: x.split(",")[0].replace('"', ''), all_tickers))

def extract_tickers_from_api_response(ticker_list):
    all_tickers = []
    ticker_list = ticker_list.split("\n")
    for ticker in ticker_list:
        try:
            ticker_string = findall('"([^"]*)"', ticker)[0]
            if not ticker_string.lower() == 'symbol':
                all_tickers.append(ticker_string)
        except IndexError:
            continue
    return ticker_list

def get_api_response(exchange):
    request = Request(get_api_url(exchange))
    response = urlopen(request)
    return response.read()


def _write_tickers_to_file(exchange, file_data_string, file_path=None):
    if not file_path:
        file_path = path.join(path.join(path.dirname(path.abspath(__file__)), TICKERS_FOLDER), (exchange + '.txt'))
    else:
        file_path = path.join(file_path, exchange + '.txt')
    with open(file_path, 'w') as f:
       f.write(file_data_string)

def get_api_url(exchange):
    return API_URL.format(exchange)


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
        if not any(sym in ticker for sym in FILTERED_SYMBOLS):
            filtered_list.append(ticker)
    filtered_list.sort()
    return filtered_list