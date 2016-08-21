from datetime import datetime

from AnalyseIchimoku import analyze_ichimoku
from EmailSender import send_email
from Logger import get_logger

logger = get_logger()

def run():
    if datetime.today().weekday() not in (4, 5):
        logger.info("Starting ichimoku screener")
        start_time = datetime.now()
        ichi_dict = (analyze_ichimoku())
        send_email(ichi_dict)
        end_time = datetime.now()
        logger.info("Finished screening. Total time: {}".format(end_time - start_time))

if __name__ == "__main__":
    run()
