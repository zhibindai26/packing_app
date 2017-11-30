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

output_file = destination + '_' + str(datetime.today().year) + '_packing.txt'
checkbox = '[ ] '

# create country dictionary
us_cities = {}
def create_country_state_dict():
    with open("us_cities.csv", "r") as infile:
        for line in infile:
            row = line.strip()
            row = row.split(',')
            city = row[0].strip()
            state = row[1].strip()
            us_cities[city] = state

create_country_state_dict()

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
    from email.mime.base import MIMEBase
    from email import encoders

    email_user = 'zhibin.app@gmail.com'
    email_password = '40z*U^96eXXk'
    email_send = 'zhibindai26@gmail.com'

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

def toiletries():
    toiletries_list = ['razor', 'toothbrush', 'floss', 'deodorant', 'mouth guard', 'facewash/soap',
                        'pomade', 'aspirin', 'lotion/oil', 'q-tips', 'tweezers', 'antacid']
    toiletries_list.sort()

    with open(output_file, 'a') as outfile:
        outfile.write('\n')
        outfile.write('TOILETRIES')
        outfile.write('\n')
        for i in toiletries_list:
            outfile.write(checkbox + i.capitalize())
            outfile.write('\n')

def electronics():
    electronics_list = ['laptop/charger', 'phone/charger', 'headphones', 'portable charger']
    electronics_list.sort()

    with open(output_file, 'a') as outfile:
        outfile.write('\n')
        outfile.write('ELECTRONICS')
        outfile.write('\n')
        for i in electronics_list:
            outfile.write(checkbox + i.capitalize())
            outfile.write('\n')

def accessories():
    mandatory_accessories = ['gum', 'chapstick', 'water bottle', 'sleep mask',
                            'plastic bags', 'book', 'selfie stick']
    mandatory_accessories.sort()

    with open(output_file, 'a') as outfile:
        outfile.write('\n')
        outfile.write('ACCESSORIES')
        outfile.write('\n')
        for i in mandatory_accessories:
            outfile.write(checkbox + i.capitalize())
            outfile.write('\n')
        if rain is True or trip_length > 4:
            outfile.write(checkbox + 'Umbrella')
            outfile.write('\n')
        if sunshine is True:
            outfile.write(checkbox + 'Sunglasses')
            outfile.write('\n')

def id():
    with open(output_file, 'a') as outfile:
        outfile.write('\n')
        outfile.write('ID')
        outfile.write('\n')
        outfile.write('[ ] Passport')
        outfile.write('\n')
        outfile.write('[ ] Charging Converter')

def regular_clothes():
    clothes_dict = {
    'Boxers': trip_length + 1, 'Socks': trip_length + 1,
    'Athletic Shorts': ceil(trip_length / 5), 'Inside Shirts': ceil(trip_length / 2),
    'Collared Shirts': '', 'Outside T-Shirts': '', 'Sweaters': '',
    'Jeans': '', 'Outside Shorts': '', 'Light Jacket': '', 'Heavy Jacket': ''
    }

    cold_accessories = ['Beanie', 'Gloves', 'Leggings']
    nice_clothes_ls = ['Nice Shirt', 'Nice Shoes', 'Slacks']
    footwear = ['Sneakers', 'Slippers']
    swimwear = 'Swimwear'

    # get counts for items

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
        clothes_dict['Inside Shirts'] = ceil(trip_length / 1.5)
    elif avg_temp <= cold:
        clothes_dict['Collared Shirts'] = ceil(trip_length / 4)
        clothes_dict['Sweaters'] = ceil(trip_length / 3)
        clothes_dict['Inside Shirts'] = ceil(trip_length / 1.5)

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
        clothes_dict['Heavy Jacket'] = ceil(trip_length / 4)
    elif avg_temp >= chilly and avg_temp < cool:
        clothes_dict['Heavy Jacket'] = ceil(trip_length / 8)
        clothes_dict['Light Jacket'] = ceil(trip_length / 8)
    elif avg_temp >= cool and avg_temp < warm:
        clothes_dict['Light Jacket'] = ceil(trip_length / 4)

    if laundry == 'YES':
        for key, value in clothes_dict.iteritems():
            if clothes_dict[key] != '':
                clothes_dict[key] = int(value) / 2

    # output to file
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

        for i in footwear:
            outfile.write(checkbox + i)
            outfile.write('\n')

        if avg_low <= cold:
            for i in cold_accessories:
                outfile.write(checkbox + i)
                outfile.write('\n')

        if avg_high >= hot and config.get('main', 'swimming').upper() == 'YES':
            outfile.write(checkbox + swimwear)
            outfile.write('\n')

        if nice_clothes == 'YES':
            outfile.write('-----------------------------------------')
            outfile.write('\n')
            for i in nice_clothes_ls:
                outfile.write(checkbox + i)
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
    toiletries()
    electronics()
    accessories()

    if config.get('main', 'international').upper() == 'YES':
        id()

    if config.get('main', 'travel_guide').upper() == 'YES':
        import pdfkit
        pdfkit.from_url('http://wikitravel.org/en/' + destination_underscore,
                        destination + '_Travel_Guide' + '.pdf')

    send_email()
