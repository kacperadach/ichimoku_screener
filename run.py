import datetime

from AnalyseIchimoku import analyze_ichimoku
from EmailSender import send_email

def run():
    if datetime.datetime.today().weekday() not in (4, 5):
        ichi_dict = (analyze_ichimoku())
        send_email(ichi_dict)
        # send_email({
        #     'overlap': [],
        #     'cross_above': [],
        #     'cross_below': [],
        #     'cross_inside': [],
        #     'cloud_fold': [],
        #     'price_leaving_cloud': []
        # })

if __name__ == "__main__":
    run()