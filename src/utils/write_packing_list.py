import math
from properties.constants import *
ceil = math.ceil


class WriteItems:
    def __init__(self, trip_details, output_path, year, month, weather_details):
        self.item_list = trip_details.item_list
        self.destination = trip_details.destination
        self.trip_length = trip_details.trip_length
        self.international = trip_details.international
        self.laundry = trip_details.laundry
        self.nice_clothes = trip_details.nice_clothes
        self.swimming = trip_details.swimming
        self.checkbox = '[   ] '
        self.year = year
        self.month = month
        self.output_path = output_path
        self.weather_details = weather_details

    def write_header(self):
        with open(self.output_path, 'w') as outfile:
            outfile.write('Packing List For ' + str(self.month) + ' '
                          + str(self.year) + ' ' + self.destination.upper() + ' Trip')
            outfile.write('\n')
            outfile.write(str(int(self.trip_length)) + ' Days' + ' | ' +
                          'Temps: Avg High: ' + str(self.weather_details["avg_high"]) + ', ' + 'Avg Low: '
                          + str(self.weather_details["avg_low"]))
            outfile.write('\n')
            outfile.write('\n')

    # create items dictionary
    def create_items_dict(self):
        items_dict = {}
        with open("csv\\" + self.item_list, "r") as infile:
            next(infile)
            for line in infile:
                row = line.strip()
                row = row.split(',')
                item = row[0].strip().lower()
                category = row[1].strip()
                items_dict[item] = category
        return items_dict

    def non_clothes_items(self, items_dict):
        with open(self.output_path, 'a') as outfile:
            outfile.write('\n')
            outfile.write('TOILETRIES')
            outfile.write('\n')
            for key, value in items_dict.iteritems():
                if value == 'Toiletry':
                    outfile.write(self.checkbox + key.capitalize())
                    outfile.write('\n')

            outfile.write('\n')
            outfile.write('ELECTRONICS')
            outfile.write('\n')
            for key, value in items_dict.iteritems():
                if value == 'Electronics':
                    outfile.write(self.checkbox + key.capitalize())
                    outfile.write('\n')

            outfile.write('\n')
            outfile.write('ACCESSORIES')
            outfile.write('\n')
            for key, value in items_dict.iteritems():
                if value == 'Mandatory Accessories':
                    outfile.write(self.checkbox + key.capitalize())
                    outfile.write('\n')

            if self.weather_details["rain"] is True:
                outfile.write(self.checkbox + 'Umbrella')
                outfile.write('\n')

            if self.international.lower() == 'yes':
                outfile.write('\n')
                outfile.write('ID')
                outfile.write('\n')
                for key, value in items_dict.iteritems():
                    if value == 'ID':
                        outfile.write(self.checkbox + key.capitalize())
                        outfile.write('\n')

    def regular_clothes(self, items_dict):
        avg_temp = self.weather_details["avg_temp"]
        avg_high = self.weather_details["avg_high"]
        avg_low = self.weather_details["avg_low"]

        if "zd" in self.item_list:
            constants_map = ZHIBIN_ITEMS
        else:
            constants_map = KSEO_ITEMS

        clothes_dict = {}
        for key, value in items_dict.iteritems():
            if value == 'Clothes':
                clothes_dict[key] = ''

        for key in constants_map["ADD"]:
            if key.lower() in clothes_dict.keys():
                clothes_dict[key] = self.trip_length + constants_map["ADD"][key]

        # shirt counts
        if avg_temp >= HOT:
            for key in constants_map["HOT_CLOTHES"].keys():
                if key.lower() in clothes_dict.keys():
                    clothes_dict[key] = ceil(self.trip_length / constants_map["HOT_CLOTHES"][key])
        elif WARM <= avg_temp < HOT:
            for key in constants_map["HOT_WARM_CLOTHES"].keys():
                if key.lower() in clothes_dict.keys():
                    clothes_dict[key] = ceil(self.trip_length / constants_map["HOT_WARM_CLOTHES"][key])
        elif COOL <= avg_temp < WARM:
            for key in constants_map["WARM_COOL_CLOTHES"].keys():
                if key.lower() in clothes_dict.keys():
                    clothes_dict[key] = ceil(self.trip_length / constants_map["WARM_COOL_CLOTHES"][key])
        elif CHILLY <= avg_temp < COOL:
            for key in constants_map["COOL_CHILLY_CLOTHES"]:
                if key.lower == constants_map["COOL_CHILLY_CLOTHES"]["outside t-shirts"]:
                    clothes_dict['Outside T-Shirts'] = 1
                elif key.lower() in clothes_dict.keys():
                    clothes_dict[key] = ceil(self.trip_length / constants_map["COOL_CHILLY_CLOTHES"][key])
        elif avg_temp <= COLD:
            for key in constants_map["COLD_CLOTHES"].keys():
                if key.lower() in clothes_dict.keys():
                    clothes_dict[key] = ceil(self.trip_length / constants_map["COLD_CLOTHES"][key])

        if self.laundry == 'YES':
            for key, value in clothes_dict.iteritems():
                if clothes_dict[key] != '':
                    clothes_dict[key] = ceil(int(value) / 1.5)

        # write to file
        with open(self.output_path, 'a') as outfile:
            outfile.write('\n')
            outfile.write('CLOTHES')
            outfile.write('\n')

            sorted_clothes = []
            for key, value in clothes_dict.iteritems():
                if value != '':
                    sorted_clothes.append(key)

            sorted_clothes.sort()
            for i in sorted_clothes:
                outfile.write(self.checkbox + i + ' - ' + str(clothes_dict[i]))
                outfile.write('\n')

            for key, value in items_dict.iteritems():
                if avg_low <= COLD:
                    if value == 'Cold Accessories':
                        outfile.write(self.checkbox + key.capitalize())
                        outfile.write('\n')

                if self.nice_clothes == 'YES':
                    if value == 'Formal Clothes':
                        outfile.write(self.checkbox + key.capitalize())
                        outfile.write('\n')

                if avg_high >= HOT and self.swimming.lower() == 'yes':
                    if value == 'Swimwear':
                        outfile.write(self.checkbox + key.capitalize())
                        outfile.write('\n')

                if value == 'Footwear':
                    outfile.write(self.checkbox + key.capitalize())
                    outfile.write('\n')

    def write_list(self):
        items_dict = self.create_items_dict()
        self.write_header()
        self.non_clothes_items(items_dict)
        self.regular_clothes(items_dict)
