from datetime import datetime

from AnalyseIchimoku import analyze_ichimoku
from EmailSender import send_email

def run():
    if datetime.today().weekday() not in (4, 5):
        ichi_dict = (analyze_ichimoku())
        send_email(ichi_dict)

if __name__ == "__main__":
    run()
