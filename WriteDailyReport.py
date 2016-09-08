from os import path
from datetime import date

from Constants import DAILY_REPORTS_FOLDER, DAILY_REPORTS_ENDING

def write_daily_report(message_body):
    daily_report_file = path.join(path.join(path.dirname(path.abspath(__file__)), DAILY_REPORTS_FOLDER),
                                  (date.today().isoformat() + DAILY_REPORTS_ENDING))
    daily_report = open(daily_report_file, 'w')
    daily_report.write(strip_html_from_body(message_body._payload))

def strip_html_from_body(payload):
    body_message = ""
    in_html = False
    for char in payload:
        if char == "<":
            in_html = True
        elif char == ">":
            in_html = False
        else:
            if not in_html:
                body_message += char
    return body_message