from datetime import date
from os import path

from Constants import DAILY_REPORTS_FOLDER, DAILY_REPORTS_ENDING

def read_daily_report(report_path=None):
    if not report_path:
        report_path = get_default_file_path()
    f = open(report_path, 'r')
    lines = remove_unnecessary_lines(f.readlines())
    return extract_tickers_into_dict(lines)

def get_default_file_path():
    return path.join(path.join(path.dirname(path.abspath(__file__)), DAILY_REPORTS_FOLDER), (date.today().isoformat() + DAILY_REPORTS_ENDING))

def remove_unnecessary_lines(lines):
    return map(lambda x: x.strip(), filter(lambda x: x.strip() != "", lines))

def extract_tickers_into_dict(lines):
    ichi_dict = {
        'cross_above': [],
        'cross_inside': [],
        'cross_below': [],
        'price_leaving_cloud': [],
        'cloud_fold': [],
        'overlap': []
    }
    for line in lines:
        if line.split()[0] == 'Daily':
            continue
        elif line == 'TK cross and Bullish Cloud Fold:':
            tickers = lines[lines.index(line) + 1]
            ichi_dict['overlap'] = map(lambda x: x.strip(','), tickers.split())
        elif line == 'Crosses above the cloud:':
            tickers = lines[lines.index(line) + 1]
            ichi_dict['cross_above'] = map(lambda x: x.strip(','), tickers.split())
        elif line == 'Crosses inside the cloud:':
            tickers = lines[lines.index(line) + 1]
            ichi_dict['cross_inside'] = map(lambda x: x.strip(','), tickers.split())
        elif line == 'Crosses below the cloud:':
            tickers = lines[lines.index(line) + 1]
            ichi_dict['cross_below'] = map(lambda x: x.strip(','), tickers.split())
        elif line == 'Bullish Price Action leaving the cloud:':
            tickers = lines[lines.index(line) + 1]
            ichi_dict['price_leaving_cloud'] = map(lambda x: x.strip(','), tickers.split())
        elif line == 'Bullish Cloud Fold:':
            tickers = lines[lines.index(line) + 1]
            ichi_dict['cloud_fold'] = map(lambda x: x.strip(','), tickers.split())
    return ichi_dict
