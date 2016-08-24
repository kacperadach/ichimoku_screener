from datetime import datetime
from os import getenv

from AnalyseIchimoku import analyze_ichimoku
from EmailSender import send_email
from Logger import get_logger

from GetStockTickers import get_all_tickers_from_ftp

logger = get_logger()

def run():
    if datetime.today().weekday() not in (4, 5):
        logger.info("Starting ichimoku screener")
        start_time = datetime.now()
        logger.info("Filter Settings: {}".format(_get_filter_settings()))
        ichi_dict = (analyze_ichimoku())
        send_email(ichi_dict)
        end_time = datetime.now()
        logger.info("Finished screening. Total time: {}".format(end_time - start_time))

def _get_filter_settings():
    return {
        "min_stock_value": getenv('MIN_STOCK_VALUE', 1),
        "volume_min": getenv('VOLUME_MIN', 400000),
        "market_cap_min": getenv('MARKET_CAP_MIN', 1000000000),
        "pe_max": getenv('PE_MAX', 50),
        "pe_min": getenv('PE_MIN', 0)
    }

if __name__ == "__main__":
    run()

