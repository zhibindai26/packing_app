import math
from constants import *
ceil = math.ceil


class WriteItems:
    def __init__(self, trip_details, weather_details):
        self.traveler = trip_details["traveler"].upper()
        self.item_list = "zd_items.csv" if self.traveler == "ZD" else "ks_items.csv"
        self.trip_length = int(trip_details["duration"])
        self.international = trip_details["international"].capitalize()
        self.laundry = trip_details["laundry"].capitalize()
        self.nice_clothes = trip_details["nice_clothes"].capitalize()
        self.swimming = trip_details["swimming"].capitalize()
        self.weather_details = weather_details
        self.avg_temp = weather_details["avg_temp"]
        self.checkbox = "[  ]"
        self.packing_list = []

    # create items dictionary
    def create_items_dict(self):
        items_dict = {}
        with open("./csv/" + self.item_list, "r") as infile:
            next(infile)
            for line in infile:
                row = line.strip().split(',')
                item = row[0].title()
                category = row[1].title()
                category_type = row[2].title()
                items_dict[item] = [category, category_type]
        return items_dict

    def non_count(self, items_dict):
        for key, value in items_dict.items():
            item_obj = {
                    "item": key,
                    "category": value[0],
                    "count": 1,
                    "checkbox": self.checkbox
                }
            if value[1] == "Non-Clothes":
                if value[0] not in ["Rain", "Id"]:
                    self.packing_list.append(item_obj)
                elif (value[0] == "Rain" and self.weather_details["rain"] is True) or (value[0] == "Id" and self.international == 'Yes'):
                    self.packing_list.append(item_obj)
            elif value[1] == "Non-Count Clothes":
                if (value[0] == "Footwear") or \
                    (value[0] == "Cold Accessories" and self.avg_temp <= COOL) or \
                    (value[0] == "Swimwear" and self.swimming == "Yes") or \
                    (value[0] == "Formal Clothes" and self.nice_clothes == "Yes"):
                    self.packing_list.append(item_obj)

    def regular_clothes(self, items_dict):
        constants_map = ZD_ITEMS if self.traveler == "ZD" else KS_ITEMS
        laundry_trip_length = ceil(self.trip_length / 1.5) if self.laundry == 'Yes' else self.trip_length

        clothes_map_to_use = None
        if self.avg_temp >= HOT:
            clothes_map_to_use = constants_map["HOT_CLOTHES"]
        elif WARM <= self.avg_temp < HOT:
            clothes_map_to_use = constants_map["HOT_WARM_CLOTHES"]
        elif COOL <= self.avg_temp < WARM:
            clothes_map_to_use = constants_map["WARM_COOL_CLOTHES"]
        elif CHILLY <= self.avg_temp < COOL:
            clothes_map_to_use = constants_map["COOL_CHILLY_CLOTHES"]
        elif self.avg_temp < CHILLY:
            clothes_map_to_use = constants_map["COLD_CLOTHES"]
        
        # doing the clothes with counts based on weather
        for key, value in items_dict.items():
            if value[1] == "Clothes":
                if key in clothes_map_to_use.keys():
                    item_obj = {
                            "item": key,
                            "category": value[0],
                            "count": ceil(laundry_trip_length / clothes_map_to_use[key]),
                            "checkbox": self.checkbox
                        }
                    self.packing_list.append(item_obj)
                elif key in constants_map["ADD"].keys():
                    item_obj = {
                            "item": key,
                            "category": value[0],
                            "count": laundry_trip_length + constants_map["ADD"][key],
                            "checkbox": self.checkbox
                        }
                    self.packing_list.append(item_obj)

    def create_list(self):
        items_dict = self.create_items_dict()
        self.non_count(items_dict)
        self.regular_clothes(items_dict)
        return self.packing_list
