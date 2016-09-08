from datetime import date

# Getting holidays from https://www.nyse.com/markets/hours-calendars

TRADING_HOLIDAYS = [
    date(2016, 9, 5),
    date(2016, 11, 24),
    date(2016, 12, 26),
    date(2017, 1, 2),
    date(2017, 1, 16),
    date(2017, 2, 20),
    date(2017, 4, 14),
    date(2017, 5, 29),
    date(2017, 7, 4),
    date(2017, 9, 4),
    date(2017, 11, 23),
    date(2017, 12, 25)
]

COMMASPACE = ', '

DAILY_REPORTS_FOLDER = 'daily_reports'

DAILY_REPORTS_ENDING = '_report.txt'

CLIENT_SECRET_FILE = 'json/client_secret.json'

APPLICATION_NAME = 'ichimokuemaillist'

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

FILES = ["amex.txt", "nasdaq.txt", "nyse.txt"]

SPECIFIC_PATH = 'tickers/all_tickers.txt'

IGNORED_STRINGS = ('SYMBOL', )

FTP_ADDRESS = 'ftp.nasdaqtrader.com'

FTP_CWD = 'SymbolDirectory'

NASDAQ_FILE = 'nasdaqlisted.txt'

OTHER_FILE = 'otherlisted.txt'

FTP_DELIMITER = '|'

FILTERED_SYMBOLS = ('^', '.', '$')
