from smtplib import SMTP
from datetime import datetime
from os import environ, path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from GoogleSheetsAPI import get_email_addresses
from ReadDailyReport import read_daily_report
from EmailSender import get_message_body

COMMASPACE = ', '

a = read_daily_report()
# try:
#     msg = MIMEMultipart()
#     msg['Subject'] = 'Ichimoku stock screener for {}'.format(datetime.now().isoformat().split("T")[0])
#     msg['From'] = environ['EMAIL_ADDRESS']
#     family = get_email_addresses()
#     msg['To'] = COMMASPACE.join(family)
#     message_body = get_message_body(a)
#     msg.attach(message_body)
#
#     s = SMTP('smtp.gmail.com:587')  # standard address + port for using gmail as stmp
#     s.ehlo()
#     s.starttls()
#     s.login(environ['EMAIL_ADDRESS'], environ['EMAIL_PASSWORD'])
#     #s.sendmail(environ['EMAIL_ADDRESS'], family, msg.as_string())
#     s.quit()
# except Exception, e:
#     print e