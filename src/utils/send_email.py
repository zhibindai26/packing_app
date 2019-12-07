import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from utils.get_trip_details import email_user, email_password, email_recipient, destination


def send_email(email_file):
    subject = 'Packing List for {} {} Trip'.format(destination.upper(), str(datetime.today().year))

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_recipient
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

    server.sendmail(email_user, email_recipient, text)
    server.quit()
