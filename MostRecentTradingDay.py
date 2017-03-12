from datetime import date, timedelta

from Constants import TRADING_HOLIDAYS
from Logger import get_logger

logger = get_logger()

def get_most_recent_trading_day():
    today = date.today()
    if today in TRADING_HOLIDAYS:
        today = today - timedelta(days=1)
    logger.info("Using {} as today.".format(today))
    if today.weekday() < 5:
        last_trading_day = today
    elif today.weekday() == 5:
        last_trading_day = (today - timedelta(days=1))
    else:
        last_trading_day = (today - timedelta(days=2))
    logger.info("Using {} as most recent trading day.".format(last_trading_day))
    return last_trading_day.isoformat()