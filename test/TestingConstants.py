from os import path

BASE_PATH = path.dirname(path.abspath(__file__))

SPECIFIC = 'temp'

SPECIFIC_PATH = path.join(SPECIFIC, 'all_tickers.txt')

TEMP_PATH = path.join(BASE_PATH, SPECIFIC)

TEST_TICKERS = ('AAL', 'GILD', 'VIAB', 'MDLZ', 'FITB', 'BIDU', 'ERIC', 'SWKS')