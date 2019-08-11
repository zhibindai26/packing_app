import math
from properties.constants import *
ceil = math.ceil


class WriteItems:
    def __init__(self, trip_details, output_path, weather_details):
        self.item_list = trip_details.item_list
        self.trip_length = trip_details.trip_length
        self.international = trip_details.international
        self.laundry = trip_details.laundry
        self.nice_clothes = trip_details.nice_clothes
        self.swimming = trip_details.swimming
        self.checkbox = '[   ] '
        self.output_path = output_path
        self.weather_details = weather_details

    # create items dictionary
    def create_items_dict(self):
        items_dict = {}
        with open("csv\\" + self.item_list, "r") as infile:
            next(infile)
            for line in infile:
                row = line.strip()
                row = row.split(',')
                item = row[0].strip()
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

        clothes_dict = {}
        for key, value in items_dict.iteritems():
            if value == 'Clothes':
                clothes_dict[key] = ''

        clothes_dict['Boxers'] = self.trip_length + BOXERS
        clothes_dict['Socks'] = self.trip_length + SOCKS
        clothes_dict['Athletic Shorts'] = ceil(self.trip_length / ATHLETIC_SHORTS)
        clothes_dict['Sweatpants'] = ceil(self.trip_length / SWEATPANTS)
        clothes_dict['Inside Shirts'] = ceil(self.trip_length / INSIDE_SHIRTS)

        # shirt counts
        if avg_temp >= HOT:
            clothes_dict['Collared Shirts'] = ceil(self.trip_length / HOT_CLOTHES["COLLARED SHIRTS"])
            clothes_dict['Outside T-Shirts'] = ceil(self.trip_length / HOT_CLOTHES["OUTSIDE T SHIRTS"])
            clothes_dict['Inside Shirts'] = ceil(self.trip_length / HOT_CLOTHES["INSIDE SHIRTS"])
        elif WARM <= avg_temp < HOT:
            clothes_dict['Collared Shirts'] = ceil(self.trip_length / HOT_WARM_CLOTHES["COLLARED SHIRTS"])
            clothes_dict['Outside T-Shirts'] = ceil(self.trip_length / HOT_WARM_CLOTHES["OUTSIDE T SHIRTS"])
        elif COOL <= avg_temp < WARM:
            clothes_dict['Collared Shirts'] = ceil(self.trip_length / WARM_COOL_CLOTHES["COLLARED SHIRTS"])
            clothes_dict['Outside T-Shirts'] = ceil(self.trip_length / WARM_COOL_CLOTHES["OUTSIDE T SHIRTS"])
            clothes_dict['Sweaters'] = ceil(self.trip_length / WARM_COOL_CLOTHES["SWEATERS"])
        elif CHILLY <= avg_temp < COOL:
            clothes_dict['Collared Shirts'] = ceil(self.trip_length / COOL_CHILLY_CLOTHES["COLLARED SHIRTS"])
            clothes_dict['Outside T-Shirts'] = 1
            clothes_dict['Sweaters'] = ceil(self.trip_length / COOL_CHILLY_CLOTHES["SWEATERS"])
        elif avg_temp <= COLD:
            clothes_dict['Collared Shirts'] = ceil(self.trip_length / COLD_CLOTHES["COLLARED SHIRTS"])
            clothes_dict['Sweaters'] = ceil(self.trip_length / COLD_CLOTHES["SWEATERS"])

        # jeans counts
        if avg_high >= WARM:
            clothes_dict['Jeans'] = ceil(self.trip_length / HOT_CLOTHES["JEANS"])
        else:
            clothes_dict['Jeans'] = ceil(self.trip_length / COOL_CHILLY_CLOTHES["JEANS"])

        # shorts counts
        if avg_temp >= WARM:
            clothes_dict['Outside Shorts'] = ceil(self.trip_length / HOT_WARM_CLOTHES["OUTSIDE SHORTS"])

        # jacket counts
        if avg_low <= COLD:
            clothes_dict['Heavy Jacket'] = ceil(self.trip_length / COLD_CLOTHES["HEAVY JACKET"])
        elif CHILLY <= avg_temp < COOL:
            clothes_dict['Heavy Jacket'] = ceil(self.trip_length / COOL_CHILLY_CLOTHES["HEAVY JACKET"])
            clothes_dict['Light Jacket'] = ceil(self.trip_length / COOL_CHILLY_CLOTHES["LIGHT JACKET"])
        elif COOL <= avg_temp < WARM:
            clothes_dict['Light Jacket'] = ceil(self.trip_length / WARM_COOL_CLOTHES["LIGHT JACKET"])

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
                        outfile.write(self.checkbox + key)
                        outfile.write('\n')

                if self.nice_clothes == 'YES':
                    if value == 'Formal Clothes':
                        outfile.write(self.checkbox + key)
                        outfile.write('\n')

                if avg_high >= HOT and self.swimming.lower() == 'yes':
                    if value == 'Swimwear':
                        outfile.write(self.checkbox + key)
                        outfile.write('\n')

                if value == 'Footwear':
                    outfile.write(self.checkbox + key)
                    outfile.write('\n')

    def write_list(self):
        items_dict = self.create_items_dict()
        self.non_clothes_items(items_dict)
        self.regular_clothes(items_dict)
