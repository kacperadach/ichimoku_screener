from datetime import datetime, timedelta

from yahoo_finance import Share

from constants import logger


def get_stock_data(ticker):
    try:
        s = Share(ticker)
        today = datetime.today()
        start_date = datetime.today() - timedelta(days=150)
        today_string = today.isoformat().split("T")[0]
        start_date_string = start_date.isoformat().split("T")[0]
        data = s.get_historical(start_date_string, today_string)
        if filter_stocks(s, data) or len(data) < 104 or not ensure_most_recent_data(data):
            return
        else:
            return data
    except:
        logger.error("Daily data not found for {}".format(ticker))
        return

def ensure_most_recent_data(data):
    today = datetime.today()
    if today.weekday() < 5:
        last_trading_day = today.isoformat().isoformat().split("T")[0]
    elif today.weekday() == 5:
        last_trading_day = (today - timedelta(days=1)).isoformat().split("T")[0]
    else:
        last_trading_day = (today - timedelta(days=2)).isoformat().split("T")[0]
    return data[0]['Date'] == last_trading_day



def filter_stocks(s, data):
    try:
        if not data:
            return True
        elif float(data[0]['Close']) <= 1 or \
            not _over_market_cap_filter(s.get_market_cap()) or \
            not _over_pe_filter(s.get_price_earnings_ratio()) or \
            not s.get_avg_daily_volume() or \
            float(s.get_avg_daily_volume()) < 400000 or \
            (float(s.get_year_high()) * .99) <= float(data[0]['High']):
            return True
        else:
            return False
    except:
        return True

def _over_market_cap_filter(market_cap_string):
    try:
        return market_cap_string[-1] == 'B'
    except TypeError:
        return False

def _over_pe_filter(pe_string):
    try:
        return float(pe_string) < 50 and float(pe_string) > 0
    except:
        return False