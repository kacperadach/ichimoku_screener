from datetime import date, datetime, timedelta
from os import getenv

from yahoo_finance import Share

from Logger import get_logger
from MostRecentTradingDay import get_most_recent_trading_day

logger = get_logger()
LAST_TRADING_DAY = get_most_recent_trading_day()

def get_stock_data(ticker):
    try:
        s = Share(ticker)
        today = datetime.today()
        start_date = datetime.today() - timedelta(days=150)
        today_string = today.isoformat().split("T")[0]
        start_date_string = start_date.isoformat().split("T")[0]
        data = s.get_historical(start_date_string, today_string)
        if filter_stocks(s, data) or len(data) < 104 or not ensure_most_recent_data(data, LAST_TRADING_DAY):
            logger.info("Filtered data for {}".format(ticker))
            return
        else:
            return data
    except:
        logger.error("Daily data not found for {}".format(ticker))
        return

def ensure_most_recent_data(data, last_trading_day):
    return data[0]['Date'] == last_trading_day

def filter_stocks(s, data):
    try:
        if not data:
            return True
        elif not _over_min_stock_value(data[0]['Close']) or \
            not _over_market_cap_filter(s.get_market_cap()) or \
            not _over_pe_filter(s.get_price_earnings_ratio()) or \
            not s.get_avg_daily_volume() or \
            not _over_volume_filter(s.get_avg_daily_volume()) or \
            (float(s.get_year_high()) * .99) <= float(data[0]['High']):
            return True
        else:
            return False
    except:
        return True

def _over_min_stock_value(last_close):
    try:
        return float(last_close) >= float(getenv('MIN_STOCK_VALUE', 1))
    except:
        return False

def _over_volume_filter(volume):
    try:
        return float(volume) >= float(getenv('VOLUME_MIN', 400000))
    except:
        return False

def _over_market_cap_filter(market_cap_string):
    try:
        return _parse_market_cap_string(market_cap_string) >= float(getenv('MARKET_CAP_MIN', 1000000000))
    except:
        return False

def _over_pe_filter(pe_string):
    try:
        return float(pe_string) < float(getenv('PE_MAX', 50)) and float(pe_string) > float(getenv('PE_MIN', 0))
    except:
        return False

def _parse_market_cap_string(market_cap_string):
    if market_cap_string[-1].upper() == 'B':
        return 1000000000 * float(market_cap_string[0:-1])
    elif market_cap_string[-1].upper() == 'M':
        return 1000000 * float(market_cap_string[0:-1])
    else:
        logger.info("Market cap not in millions or billions, {}".format(market_cap_string))
        return 0