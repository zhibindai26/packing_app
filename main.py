#!/usr/bin/env python

from ConfigParser import ConfigParser
import math
import urllib2
import json
from datetime import datetime

ceil = math.ceil
config = ConfigParser()
config.read('trip_details.ini')

destination = config.get('main', 'destination')
destination_underscore = destination.replace(' ', '_')
trip_length = float(config.get('main', 'days'))
laundry = config.get('main', 'laundry').upper()
nice_clothes = config.get('main', 'nice_clothes').upper()

email_config = ConfigParser()
email_config.read('email_config.ini')

output_file = destination + '_' + str(datetime.today().year) + '_packing.txt'
checkbox = '[ ] '

# create items dictionary
items_dict = {}
us_cities = {}
def create_items_and_location_dictionaries():
    with open("csv\items.csv", "r") as infile:
        for line in infile:
            row = line.strip()
            row = row.split(',')
            item = row[0].strip()
            category = row[1].strip()
            items_dict[item] = category

    with open("csv\us_cities.csv", "r") as infile:
        for line in infile:
            row = line.strip()
            row = row.split(',')
            city = row[0].strip()
            state = row[1].strip()
            us_cities[city] = state

create_items_and_location_dictionaries()

# get weather
avg_high_list = []
avg_low_list = []
precip_list = []
conditions_list = []

f = urllib2.urlopen('http://api.wunderground.com/api/cacea4c99bc7010d/forecast10day/conditions/q/%s/%s.json' %
                    (us_cities[destination], destination_underscore))
json_string = f.read()
parsed_json = json.loads(json_string)

# avg high
for day in parsed_json['forecast']['simpleforecast']['forecastday']:
    avg_high_list.append(int(day['high']['fahrenheit']))

# avg low
for day in parsed_json['forecast']['simpleforecast']['forecastday']:
    avg_low_list.append(int(day['low']['fahrenheit']))

# precipitation
for i, pop in enumerate(d['pop'] for d in parsed_json['forecast']['simpleforecast']['forecastday']):
     precip_list.append(pop)

# conditions
for i, condition in enumerate(d['conditions'] for d in parsed_json['forecast']['simpleforecast']['forecastday']):
     conditions_list.append(condition)

f.close()

delete_from_avgs = -(len(avg_high_list) - int(trip_length) - 1)

if len(avg_high_list) > int(trip_length) and delete_from_avgs != 0:
    del avg_high_list[delete_from_avgs:]
    del avg_low_list[delete_from_avgs:]
    del precip_list[delete_from_avgs:]
    del conditions_list[delete_from_avgs:]

# temps
hot = 80
warm = 70
cool = 60
chilly = 50
cold = 49
rain = False
sunshine = False

avg_high = sum(avg_high_list) / float(len(avg_high_list))
avg_low = sum(avg_low_list) / float(len(avg_low_list))
avg_temp = (avg_low + avg_high) / 2

if max(precip_list) >= 20:
    rain = True

if "Partly Cloudy" in conditions_list or "Clear" in conditions_list:
    sunshine = True

def send_email():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

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

        if rain is True or trip_length > 4:
            outfile.write(checkbox + 'Umbrella')
            outfile.write('\n')
        if sunshine is True:
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

    if laundry == 'YES':
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

            if nice_clothes == 'YES':
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

    with open(output_file, 'w') as outfile:
        outfile.write('Packing List For ' + str(datetime.now().strftime("%B")) + ' '
                        + str(datetime.today().year) + ' ' + destination + ' Trip')
        outfile.write('\n')
        outfile.write(str(int(trip_length)) + ' Days' + ' | ' +
                        'Temps: Avg High: ' + str(avg_high) + ', ' + 'Avg Low: ' + str(avg_low))
        outfile.write('\n')
        outfile.write('\n')

    regular_clothes()
    non_clothes_items()

    if config.get('main', 'travel_guide').upper() == 'YES':
       import pdfkit
       pdfkit.from_url('http://wikitravel.org/en/' + destination_underscore,
                       destination + '_Travel_Guide' + '.pdf')

    send_email()
