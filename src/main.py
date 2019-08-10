#!/usr/bin/env python
from datetime import datetime
import math
from utils import get_weather, get_trip_details, send_email
from properties.constants import *

ceil = math.ceil
destination = get_trip_details.destination
config = get_trip_details.config
trip_length = get_trip_details.trip_length


# create items dictionary
def create_items_dict():
    items_dict = {}
    item_file = get_trip_details.item_list
    with open("..\\csv\\" + item_file, "r") as infile:
        next(infile)
        for line in infile:
            row = line.strip()
            row = row.split(',')
            item = row[0].strip()
            category = row[1].strip()
            items_dict[item] = category
    return items_dict


def non_clothes_items(items_dict):
    with open(output_path, 'a') as outfile:
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

        if get_trip_details.international.lower() == 'yes':
            outfile.write('\n')
            outfile.write('ID')
            outfile.write('\n')
            for key, value in items_dict.iteritems():
                if value == 'ID':
                    outfile.write(checkbox + key.capitalize())
                    outfile.write('\n')


def regular_clothes(items_dict):
    avg_temp = get_weather.avg_temp
    avg_high = get_weather.avg_high
    avg_low = get_weather.avg_low

    clothes_dict = {}
    for key, value in items_dict.iteritems():
        if value == 'Clothes':
            clothes_dict[key] = ''

    clothes_dict['Boxers'] = trip_length + BOXERS
    clothes_dict['Socks'] = trip_length + SOCKS
    clothes_dict['Athletic Shorts'] = ceil(trip_length / ATHLETIC_SHORTS)
    clothes_dict['Sweatpants'] = ceil(trip_length / SWEATPANTS)
    clothes_dict['Inside Shirts'] = ceil(trip_length / INSIDE_SHIRTS)

    # shirt counts
    if avg_temp >= HOT:
        clothes_dict['Collared Shirts'] = ceil(trip_length / HOT_CLOTHES["COLLARED SHIRTS"])
        clothes_dict['Outside T-Shirts'] = ceil(trip_length / HOT_CLOTHES["OUTSIDE T SHIRTS"])
        clothes_dict['Inside Shirts'] = ceil(trip_length / HOT_CLOTHES["INSIDE SHIRTS"])
    elif WARM <= avg_temp < HOT:
        clothes_dict['Collared Shirts'] = ceil(trip_length / HOT_WARM_CLOTHES["COLLARED SHIRTS"])
        clothes_dict['Outside T-Shirts'] = ceil(trip_length / HOT_WARM_CLOTHES["OUTSIDE T SHIRTS"])
    elif COOL <= avg_temp < WARM:
        clothes_dict['Collared Shirts'] = ceil(trip_length / WARM_COOL_CLOTHES["COLLARED SHIRTS"])
        clothes_dict['Outside T-Shirts'] = ceil(trip_length / WARM_COOL_CLOTHES["OUTSIDE T SHIRTS"])
        clothes_dict['Sweaters'] = ceil(trip_length / WARM_COOL_CLOTHES["SWEATERS"])
    elif CHILLY <= avg_temp < COOL:
        clothes_dict['Collared Shirts'] = ceil(trip_length / COOL_CHILLY_CLOTHES["COLLARED SHIRTS"])
        clothes_dict['Outside T-Shirts'] = 1
        clothes_dict['Sweaters'] = ceil(trip_length / COOL_CHILLY_CLOTHES["SWEATERS"])
    elif avg_temp <= COLD:
        clothes_dict['Collared Shirts'] = ceil(trip_length / COLD_CLOTHES["COLLARED SHIRTS"])
        clothes_dict['Sweaters'] = ceil(trip_length / COLD_CLOTHES["SWEATERS"])

    # jeans counts
    if avg_high >= WARM:
        clothes_dict['Jeans'] = ceil(trip_length / HOT_CLOTHES["JEANS"])
    else:
        clothes_dict['Jeans'] = ceil(trip_length / COOL_CHILLY_CLOTHES["JEANS"])

    # shorts counts
    if avg_temp >= WARM:
        clothes_dict['Outside Shorts'] = ceil(trip_length / HOT_WARM_CLOTHES["OUTSIDE SHORTS"])

    # jacket counts
    if avg_low <= COLD:
        clothes_dict['Heavy Jacket'] = ceil(trip_length / COLD_CLOTHES["HEAVY JACKET"])
    elif CHILLY <= avg_temp < COOL:
        clothes_dict['Heavy Jacket'] = ceil(trip_length / COOL_CHILLY_CLOTHES["HEAVY JACKET"])
        clothes_dict['Light Jacket'] = ceil(trip_length / COOL_CHILLY_CLOTHES["LIGHT JACKET"])
    elif COOL <= avg_temp < WARM:
        clothes_dict['Light Jacket'] = ceil(trip_length / WARM_COOL_CLOTHES["LIGHT JACKET"])

    if get_trip_details.laundry == 'YES':
        for key, value in clothes_dict.iteritems():
            if clothes_dict[key] != '':
                clothes_dict[key] = ceil(int(value) / 1.5)

    # write to file
    with open(output_path, 'a') as outfile:
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
            if avg_low <= COLD:
                if value == 'Cold Accessories':
                    outfile.write(checkbox + key)
                    outfile.write('\n')

            if get_trip_details.nice_clothes == 'YES':
                if value == 'Formal Clothes':
                    outfile.write(checkbox + key)
                    outfile.write('\n')

            if avg_high >= HOT and config.get('main', 'swimming').upper() == 'YES':
                if value == 'Swimwear':
                    outfile.write(checkbox + key)
                    outfile.write('\n')

            if value == 'Footwear':
                outfile.write(checkbox + key)
                outfile.write('\n')


if __name__ == "__main__":

    from os.path import join as path_join

    output_file = destination + '_' + str(datetime.today().year) + '_packing.txt'
    output_path = path_join("trips", output_file)
    checkbox = '[ ] '

    with open(output_path, 'w') as outfile:
        outfile.write('Packing List For ' + str(datetime.now().strftime("%B")) + ' '
                      + str(datetime.today().year) + ' ' + destination + ' Trip')
        outfile.write('\n')
        outfile.write(str(int(trip_length)) + ' Days' + ' | ' +
                      'Temps: Avg High: ' + str(get_weather.avg_high) + ', ' + 'Avg Low: ' + str(get_weather.avg_low))
        outfile.write('\n')
        outfile.write('\n')

    items_dct = create_items_dict()
    regular_clothes(items_dct)
    non_clothes_items(items_dct)

    if config.get('main', 'travel_guide').upper() == 'YES':
        import pdfkit

        pdfkit.from_url('http://wikitravel.org/en/' + get_trip_details.destination_underscore,
                        destination + '_Travel_Guide' + '.pdf')

    send_email.send_email(output_path)
