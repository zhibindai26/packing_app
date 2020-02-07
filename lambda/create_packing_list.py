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
        self.packing_list = []
        self.checkbox = "[  ]"

    # create items dictionary
    def create_items_dict(self):
        items_dict = {}
        with open("./csv/" + self.item_list, "r") as infile:
            next(infile)
            for line in infile:
                row = line.strip()
                row = row.split(',')
                item = row[0].strip().title()
                category = row[1].strip().title()
                items_dict[item] = category
        return items_dict

    def non_clothes_items(self, items_dict):
        non_clothes = ["Toiletry", "Electronics", "Mandatory Accessories"]
        for key, value in items_dict.items():
            if value in non_clothes:
                item_obj = {
                    "item": key,
                    "category": value,
                    "count": 1,
                    "checkbox": self.checkbox
                }
                self.packing_list.append(item_obj)
            elif value == "Accessories":
                if self.weather_details["rain"] is True:
                    item_obj = {
                        "item": key,
                        "category": value,
                        "count": 1,
                        "checkbox": self.checkbox
                    }
                    self.packing_list.append(item_obj)
            elif value == "Id":
                if self.international == 'Yes':
                    item_obj = {
                        "item": key,
                        "category": value,
                        "count": 1,
                        "checkbox": self.checkbox
                    }
                    self.packing_list.append(item_obj)

    def non_count_clothes(self, items_dict):
        # do the non-count items first 
        non_count_clothing = ["Cold Accessories", "Footwear"]
        for key, value in items_dict.items():
            if value in non_count_clothing:
                item_obj = {
                    "item": key,
                    "category": value,
                    "count": 1,
                    "checkbox": self.checkbox
                }
                self.packing_list.append(item_obj)
            elif value == "Swimwear" and self.swimming == "Yes":
                item_obj = {
                    "item": key,
                    "category": value,
                    "count": 1,
                    "checkbox": self.checkbox
                }
                self.packing_list.append(item_obj)
            elif value == "Formal Clothes" and self.nice_clothes == "Yes":
                item_obj = {
                    "item": key,
                    "category": value,
                    "count": 1,
                    "checkbox": self.checkbox
                }
                self.packing_list.append(item_obj)
    
    def regular_clothes(self, items_dict):
        avg_temp = self.weather_details["avg_temp"]

        constants_map = ZD_ITEMS if self.traveler == "ZD" else KS_ITEMS
        laundry_trip_length = ceil(self.trip_length / 1.5) if self.laundry == 'Yes' else self.trip_length

        clothes_map_to_use = None
        if avg_temp >= HOT:
            clothes_map_to_use = constants_map["HOT_CLOTHES"]
        elif WARM <= avg_temp < HOT:
            clothes_map_to_use = constants_map["HOT_WARM_CLOTHES"]
        elif COOL <= avg_temp < WARM:
            clothes_map_to_use = constants_map["WARM_COOL_CLOTHES"]
        elif CHILLY <= avg_temp < COOL:
            clothes_map_to_use = constants_map["COOL_CHILLY_CLOTHES"]
        elif avg_temp < CHILLY:
            clothes_map_to_use = constants_map["COLD_CLOTHES"]
        
        # doing the clothes with counts based on weather
        for key, value in items_dict.items():
            if value == "Clothes":
                if key in clothes_map_to_use.keys():
                    item_obj = {
                            "item": key,
                            "category": value,
                            "count": ceil(laundry_trip_length / clothes_map_to_use[key]),
                            "checkbox": self.checkbox
                        }
                    self.packing_list.append(item_obj)
                elif key in constants_map["ADD"].keys():
                    item_obj = {
                            "item": key,
                            "category": value,
                            "count": laundry_trip_length + constants_map["ADD"][key],
                            "checkbox": self.checkbox
                        }
                    self.packing_list.append(item_obj)

    def create_list(self):
        items_dict = self.create_items_dict()
        self.non_clothes_items(items_dict)
        self.non_count_clothes(items_dict)
        self.regular_clothes(items_dict)
        return self.packing_list
