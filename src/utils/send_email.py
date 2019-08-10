import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import get_trip_details

def send_email(email_file):
    email_config = get_trip_details.email_config
    email_user = email_config.get('main', 'email_user')
    email_password = email_config.get('main', 'email_password')
    email_send = get_trip_details.config.get('main', 'email_recipient')

    subject = 'Packing List for {} {} Trip'.format(get_trip_details.destination, str(datetime.today().year))

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = ""

    file = open(email_file, "r")
    for line in file:
        body += line

    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)


    server.sendmail(email_user, email_send, text)
    server.quit()