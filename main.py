#!/usr/bin/env python

from ConfigParser import ConfigParser
import math
from datetime import datetime
import get_weather
import get_trip_details

ceil = math.ceil
destination = get_trip_details.destination
config = get_trip_details.config
trip_length = get_trip_details.trip_length

# create items dictionary
items_dict = {}
def create_items_dict():

    with open("csv\items.csv", "r") as infile:
        for line in infile:
            row = line.strip()
            row = row.split(',')
            item = row[0].strip()
            category = row[1].strip()
            items_dict[item] = category

def send_email():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    email_config = get_trip_details.email_config

    email_user = email_config.get('main', 'email_user')
    email_password = email_config.get('main', 'email_password')
    email_send = config.get('main', 'email_recipient')

    subject = 'Packing List for {} {} Trip'.format(destination, str(datetime.today().year))

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = ""

    file = open(output_file, "r")
    for line in file:
        body += line

    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)


    server.sendmail(email_user, email_send, text)
    server.quit()

def non_clothes_items():
    with open(output_file, 'a') as outfile:
        outfile.write('\n')
        outfile.write('TOILETRIES')
        outfile.write('\n')
        for key, value in items_dict.iteritems():
            if value == 'Toiletry':
                outfile.write(checkbox + key.capitalize())
                outfile.write('\n')

        outfile.write('\n')
        outfile.write('ELECTRONICS')
        outfile.write('\n')
        for key, value in items_dict.iteritems():
            if value == 'Electronics':
                outfile.write(checkbox + key.capitalize())
                outfile.write('\n')

        outfile.write('\n')
        outfile.write('ACCESSORIES')
        outfile.write('\n')
        for key, value in items_dict.iteritems():
            if value == 'Mandatory Accessories':
                outfile.write(checkbox + key.capitalize())
                outfile.write('\n')

        if get_weather.rain is True or get_trip_details.trip_length > 4:
            outfile.write(checkbox + 'Umbrella')
            outfile.write('\n')
        if get_weather.sunshine is True:
            outfile.write(checkbox + 'Sunglasses')
            outfile.write('\n')

        if config.get('main', 'international').upper() == 'YES':
            outfile.write('\n')
            outfile.write('ID')
            outfile.write('\n')
            for key, value in items_dict.iteritems():
                if value == 'ID':
                    outfile.write(checkbox + key.capitalize())
                    outfile.write('\n')

def regular_clothes():

    avg_temp = get_weather.avg_temp
    avg_high = get_weather.avg_high
    avg_low = get_weather.avg_low
    hot = get_weather.hot
    warm = get_weather.warm
    cool = get_weather.cool
    chilly = get_weather.chilly
    cold = get_weather.cold

    clothes_dict = {}
    for key, value in items_dict.iteritems():
        if value == 'Clothes':
            clothes_dict[key] = ''

    clothes_dict['Boxers'] = trip_length + 1
    clothes_dict['Socks'] = trip_length + 1
    clothes_dict['Athletic Shorts'] = ceil(trip_length / 4)
    clothes_dict['Sweatpants'] = ceil(trip_length / 5)
    clothes_dict['Inside Shirts'] = ceil(trip_length / 1.5)

    # shirt counts
    if avg_temp >= hot:
        clothes_dict['Collared Shirts'] = ceil(trip_length / 2)
        clothes_dict['Outside T-Shirts'] = ceil(trip_length / 1.5)
        clothes_dict['Inside Shirts'] = ceil(trip_length / 3)
    elif avg_temp >= warm and avg_temp < hot:
        clothes_dict['Collared Shirts'] = ceil(trip_length / 1.5)
        clothes_dict['Outside T-Shirts'] = ceil(trip_length / 2)
    elif avg_temp >= cool and avg_temp < warm:
        clothes_dict['Collared Shirts'] = ceil(trip_length / 2)
        clothes_dict['Outside T-Shirts'] = ceil(trip_length / 4)
        clothes_dict['Sweaters'] = ceil(trip_length / 5)
    elif avg_temp >= chilly and avg_temp < cool:
        clothes_dict['Collared Shirts'] = ceil(trip_length / 2)
        clothes_dict['Outside T-Shirts'] = 1
        clothes_dict['Sweaters'] = ceil(trip_length / 3)
    elif avg_temp <= cold:
        clothes_dict['Collared Shirts'] = ceil(trip_length / 4)
        clothes_dict['Sweaters'] = ceil(trip_length / 3)

    # jeans counts
    if avg_high >= warm:
        clothes_dict['Jeans'] = ceil(trip_length / 4)
    else:
        clothes_dict['Jeans'] = ceil(trip_length / 2)

    # shorts counts
    if avg_high >= hot:
        clothes_dict['Outside Shorts'] = ceil(trip_length / 3)
    elif avg_temp >= warm and avg_temp < hot:
        clothes_dict['Outside Shorts'] = ceil(trip_length / 3)

    # jacket counts
    if avg_low <= cold:
        clothes_dict['Heavy Jacket'] = ceil(trip_length / 5)
    elif avg_temp >= chilly and avg_temp < cool:
        clothes_dict['Heavy Jacket'] = ceil(trip_length / 8)
        clothes_dict['Light Jacket'] = ceil(trip_length / 8)
    elif avg_temp >= cool and avg_temp < warm:
        clothes_dict['Light Jacket'] = ceil(trip_length / 4)

    if get_trip_details.laundry == 'YES':
        for key, value in clothes_dict.iteritems():
            if clothes_dict[key] != '':
                clothes_dict[key] = ceil(int(value) / 1.5)

    # write to file
    with open(output_file, 'a') as outfile:
        outfile.write('CLOTHES')
        outfile.write('\n')

        sorted_clothes = []
        for key, value in clothes_dict.iteritems():
            if value != '':
                sorted_clothes.append(key)

        sorted_clothes.sort()
        for i in sorted_clothes:
            outfile.write(checkbox + i + ' - ' + str(clothes_dict[i]))
            outfile.write('\n')

        for key, value in items_dict.iteritems():
            if avg_low <= cold:
                if value == 'Cold Accessories':
                    outfile.write(checkbox + key)
                    outfile.write('\n')

            if get_trip_details.nice_clothes == 'YES':
                if value == 'Formal Clothes':
                    outfile.write(checkbox + key)
                    outfile.write('\n')

            if avg_high >= hot and config.get('main', 'swimming').upper() == 'YES':
                if value == 'Swimwear':
                    outfile.write(checkbox + key)
                    outfile.write('\n')

            if value == 'Footwear':
                outfile.write(checkbox + key)
                outfile.write('\n')

if __name__ == "__main__":

    output_file = destination + '_' + str(datetime.today().year) + '_packing.txt'
    checkbox = '[ ] '

    with open(output_file, 'w') as outfile:
        outfile.write('Packing List For ' + str(datetime.now().strftime("%B")) + ' '
                        + str(datetime.today().year) + ' ' + destination + ' Trip')
        outfile.write('\n')
        outfile.write(str(int(trip_length)) + ' Days' + ' | ' +
                        'Temps: Avg High: ' + str(get_weather.avg_high) + ', ' + 'Avg Low: ' + str(get_weather.avg_low))
        outfile.write('\n')
        outfile.write('\n')

    create_items_dict()
    regular_clothes()
    non_clothes_items()

    if config.get('main', 'travel_guide').upper() == 'YES':
       import pdfkit
       pdfkit.from_url('http://wikitravel.org/en/' + get_trip_details.destination_underscore,
                       destination + '_Travel_Guide' + '.pdf')

    send_email()
