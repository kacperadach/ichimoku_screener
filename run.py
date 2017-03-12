from datetime import date, datetime
from os import getenv, path
import pickle

from AnalyseIchimoku import analyze_ichimoku
from EmailSender import send_email
from Logger import get_logger

pickle_file_name = 'ichi_dict.p'
pickle_dir = 'E;/ichimoku_screener'

logger = get_logger()

def run():
    try:
        if date.today().weekday() not in (5, 6):
            logger.info("Starting ichimoku screener")
            start_time = datetime.now()
            logger.info("Filter Settings: {}".format(_get_filter_settings()))
            ichi_dict = (analyze_ichimoku())
            try:
                pickle.dump(ichi_dict, open(path.join(pickle_dir, pickle_file_name), 'wb'))
            except:
                logger.error('Pickle could not be saved')

            send_email(ichi_dict)
            end_time = datetime.now()
            logger.info("Finished screening. Total time: {}".format(end_time - start_time))
        else:
            logger.info("Not running screener on {}".format(date.today().isoformat()))
    except Exception as e:
        logger.info("Unpected Exception: {}".format(e))

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

