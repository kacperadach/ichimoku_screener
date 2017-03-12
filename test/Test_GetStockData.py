from unittest import TestCase
from random import randint
from os import environ, getenv

from yahoo_finance import Share


from Constants import MIN_DATA_LEN, FILTER_DEFAULTS
from MostRecentTradingDay import get_most_recent_trading_day
from GetStockData import get_stock_data, get_time_period, filter_stocks, ensure_most_recent_data, _parse_market_cap_string
from GetStockTickers import get_all_tickers_from_ftp

last_trading_day = get_most_recent_trading_day()

class TestGetStockData(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGetStockData, self).__init__(*args, **kwargs)
        self.all_tickers = get_all_tickers_from_ftp()

    def get_fifty_random_tickers(self):
        ten_random_tickers = []
        for _ in range(0, 50):
            ten_random_tickers.append(self.all_tickers[randint(0, len(self.all_tickers)-1)])
        return ten_random_tickers

    def compare_lists(self, list1, list2):
        for i in range(0, len(list1) - 1):
            if cmp(list1[i], list2[i]) != 0:
                return False
        return True

    def test_get_stock_data(self):
        start, end = get_time_period()
        tickers = self.get_fifty_random_tickers()
        for ticker in tickers:
            try:
                s = Share(ticker)
                data = s.get_historical(end, start)
            except:
                continue
            if filter_stocks(s, data) or len(data) < MIN_DATA_LEN or not ensure_most_recent_data(data):
                self.assertTrue(get_stock_data(ticker, start, end) is None)
            else:
                func_data = get_stock_data(ticker, start, end)
                self.assertTrue(func_data is not None)
                self.assertTrue(len(func_data) > 0 and len(func_data) == len(data))
                self.assertTrue(self.compare_lists(data, func_data))

    def test_filter_stocks(self):
        start, end = get_time_period()
        tickers = self.get_fifty_random_tickers()
        tested = 0
        for ticker in tickers:
            if tested >= 10:
                break
            try:
                s = Share(ticker)
                data = s.get_historical(end, start)
            except:
                continue
            tested += 1
            if len(data) < MIN_DATA_LEN or data[0]['Date'] == last_trading_day:
                continue
            if not data:
                self.assertTrue(filter_stocks(s, data))
            elif data[0]['Close'] < 1:
                self.assertTrue(filter_stocks(s, data))
            elif not s.get_market_cap():
                self.assertTrue(filter_stocks(s, data))
            elif _parse_market_cap_string(s.get_market_cap()) < float(getenv('MARKET_CAP_MIN', FILTER_DEFAULTS['MARKET_CAP_MIN'])):
                self.assertTrue(filter_stocks(s, data))
            elif not s.get_price_earnings_ratio():
                self.assertTrue(filter_stocks(s, data))
            elif float(s.get_price_earnings_ratio()) >= float(getenv('PE_MAX', FILTER_DEFAULTS['PE_MAX'])) or \
                float(s.get_price_earnings_ratio()) <= float(getenv('PE_MIN', FILTER_DEFAULTS['PE_MIN'])):
                self.assertTrue(filter_stocks(s, data))
            elif not s.get_avg_daily_volume() or float(s.get_avg_daily_volume()) >= float(getenv('VOLUME_MIN', FILTER_DEFAULTS['VOLUME_MIN'])):
                self.assertTrue(filter_stocks(s, data))
            elif (float(s.get_year_high()) * .99) <= float(data[0]['High']):
                self.assertTrue(filter_stocks(s, data))
            else:
                self.assertFalse(filter_stocks(s, data))