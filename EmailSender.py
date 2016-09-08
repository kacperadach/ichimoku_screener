from smtplib import SMTP
from datetime import date
from os import environ
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from GoogleSheetsAPI import get_email_addresses
from Constants import COMMASPACE
from Logger import get_logger
from WriteDailyReport import write_daily_report

logger = get_logger()

def send_email(ichi_dict):
    if is_empty_dict(ichi_dict):
        logger.info("Empty dictionary received, not sending email.")
        return
    logger.info("Writing Daily Report")
    message_body = get_message_body(ichi_dict)
    write_daily_report(message_body)
    logger.info("Wrote Daily Report")
    logger.info("Sending email, {} tickers found.".format(sum(len(v) for v in ichi_dict.itervalues())))
    send(ichi_dict, message_body)

def send(ichi_dict, message_body):
    logger.info("Sending email, {} tickers found.".format(sum(len(v) for v in ichi_dict.itervalues())))
    try:
        msg = MIMEMultipart()
        msg['Subject'] = 'Ichimoku stock screener for {}'.format(date.today().isoformat())
        msg['From'] = environ['EMAIL_ADDRESS']
        family = get_email_addresses()
        msg['To'] = COMMASPACE.join(family)
        msg.attach(message_body)

        s = SMTP('smtp.gmail.com:587')  # standard address + port for using gmail as stmp
        s.ehlo()
        s.starttls()
        s.login(environ['EMAIL_ADDRESS'], environ['EMAIL_PASSWORD'])
        s.sendmail(environ['EMAIL_ADDRESS'], family, msg.as_string())
        s.quit()
        logger.info("Sent Email to {} addresses: {}".format(len(family), family))
    except Exception, e:
        logger.info("Error occurred while sending email: {}".format(e))

def is_empty_dict(ichi_dict):
    for _, val in ichi_dict.items():
        if val:
            return False
    return True

def get_message_body(ichi_dict):
    title_text = "Daily Time Frame Ichimoku screener for {}\n".format(date.today().isoformat())
    html_message = """
        <html>
            <body style="background-image: url('https://raw.githubusercontent.com/kacperadach/ichimoku_screener/master/images/background_pattern.jpg');">
                <div style="background-color: white;
                            margin: auto;
                            width: 60%;
                            border: 5px solid #c0c0c0;
                            padding: 10px;
                            font-family: Verdana;
                            text-align: center;">
                    <h2>{}</h2>
                    <br>
                    <h3>{}</h3>
                    <p>{}</p>
                    {}
                    <h3>{}</h3>
                    <h4>{}</h4>
                    <p>{}</p>
                    <h4>{}</h4>
                    <p>{}</p>
                    <h4>{}</h4>
                    <p>{}</p>
                    {}
                    <h3>{}</h3>
                    <h4>{}</h4>
                    <p>{}</p>
                    <h4>{}</h4>
                    <p>{}</p>
                    <hr>
                    <footer>
                        <p>{}</p>
                    </footer>
                </div>
            </body>
        </html>
    """.format(title_text,
               "" if not ichi_dict['overlap'] else "TK cross and Bullish Cloud Fold:",
               "" if not ichi_dict['overlap'] else str(ichi_dict['overlap']).replace("(", "").replace(")", "").replace("set", "").replace("[", "").replace("]", "").replace("'", ""),
               "" if not ichi_dict['overlap'] else "<br>",
               "Tenkan-Kijun Crosses:",
               "" if not ichi_dict['cross_above'] else "Crosses above the cloud:",
               "" if not ichi_dict['cross_above'] else str(ichi_dict['cross_above']).replace("[", "").replace("]", "").replace("'", ""),
               "" if not ichi_dict['cross_inside'] else "Crosses inside the cloud:",
               "" if not ichi_dict['cross_inside'] else str(ichi_dict['cross_inside']).replace("[", "").replace("]", "").replace("'", ""),
               "" if not ichi_dict['cross_below'] else "Crosses below the cloud:",
               "" if not ichi_dict['cross_below'] else str(ichi_dict['cross_below']).replace("[", "").replace("]", "").replace("'", ""),
               "<br>",
               "Cloud Movement:",
               "" if not ichi_dict['price_leaving_cloud'] else "Bullish Price Action leaving the cloud:",
               "" if not ichi_dict['price_leaving_cloud'] else str(ichi_dict['price_leaving_cloud']).replace("[", "").replace("]", "").replace("'", ""),
               "" if not ichi_dict['cloud_fold'] else "Bullish Cloud Fold:",
               "" if not ichi_dict['cloud_fold'] else str(ichi_dict['cloud_fold']).replace("[", "").replace("]", "").replace("'", ""),
               get_message_footer()
               )
    return MIMEText(html_message, 'html')

def get_message_footer():
    footer = "Don't want to get the hottest free Ichimoku Screener email available? Remove your email address from the <a style='color: #3ba722; text-decoration: none;' href='https://docs.google.com/spreadsheets/d/1yJkEd5u12niaFBPlglZO63iM4nSf-SYaXaBFhVCWX8Q/edit'>Google Sheet</a>"
    return footer
