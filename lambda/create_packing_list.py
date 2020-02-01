import math
from constants import *
ceil = math.ceil


class WriteItems:
    def __init__(self, trip_details, weather_details):
        self.traveler = trip_details["traveler"].upper()
        self.item_list = "zd_items.csv" if self.traveler == "ZD" else "ks_items.csv"
        self.trip_length = trip_details["duration"]
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
        with open("csv\\" + self.item_list, "r") as infile:
            next(infile)
            for line in infile:
                row = line.strip()
                row = row.split(',')
                item = row[0].strip().capitalize()
                category = row[1].strip()
                items_dict[item] = category
        return items_dict

    def non_clothes_items(self, items_dict):
        non_clothes = ["Toiletry", "Electronics", "Mandatory Accessories"]
        for key, value in items_dict.items():
            if value in non_clothes:
                item_obj = {
                    "item": key.capitalize(),
                    "category": value,
                    "count": 1,
                    "checkbox": self.checkbox
                }
                self.packing_list.append(item_obj)
            elif value == "Accessories":
                if self.weather_details["rain"] is True:
                    item_obj = {
                        "item": key.capitalize(),
                        "category": value,
                        "count": 1,
                        "checkbox": self.checkbox
                    }
                    self.packing_list.append(item_obj)
            elif value == "ID":
                if self.international == 'Yes':
                    item_obj = {
                        "item": key.capitalize(),
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
                    "item": key.capitalize(),
                    "category": value,
                    "count": 1,
                    "checkbox": self.checkbox
                }
                self.packing_list.append(item_obj)
            elif value == "Swimwear" and self.swimming == "Yes":
                item_obj = {
                    "item": key.capitalize(),
                    "category": value,
                    "count": 1,
                    "checkbox": self.checkbox
                }
                self.packing_list.append(item_obj)
            elif value == "Formal Clothes" and self.nice_clothes == "Yes":
                item_obj = {
                    "item": key.capitalize(),
                    "category": value,
                    "count": 1,
                    "checkbox": self.checkbox
                }
                self.packing_list.append(item_obj)
    
    def regular_clothes(self, items_dict):
        avg_temp = self.weather_details["avg_temp"]

        constants_map = ZD_ITEMS if self.traveler == "ZD" else KS_ITEMS
        laundry_trip_length = ceil(int(self.trip_length) / 1.5)

        # doing the clothes with counts based on weather
        for key, value in items_dict.items():
            if value == "Clothes" and key in constants_map["ADD"].keys():
                item_obj = {
                        "item": key.capitalize(),
                        "category": value,
                        "count": laundry_trip_length + constants_map["ADD"][key] if self.laundry == 'Yes' 
                        else self.trip_length + constants_map["ADD"][key],
                        "checkbox": self.checkbox
                    }
                self.packing_list.append(item_obj)

            if avg_temp >= HOT: 
                if value == "Clothes" and key in constants_map["HOT_CLOTHES"].keys():
                    item_obj = {
                        "item": key.capitalize(),
                        "category": value,
                        "count": ceil(laundry_trip_length / constants_map["HOT_CLOTHES"][key]) if self.laundry == 'Yes' 
                        else ceil(self.trip_length / constants_map["HOT_CLOTHES"][key]),
                        "checkbox": self.checkbox
                    }
                    self.packing_list.append(item_obj)
            elif WARM <= avg_temp < HOT:
                if value == "Clothes" and key in constants_map["HOT_WARM_CLOTHES"].keys():
                    item_obj = {
                        "item": key.capitalize(),
                        "category": value,
                        "count": ceil(laundry_trip_length / constants_map["HOT_WARM_CLOTHES"][key]) if self.laundry == 'Yes' 
                        else ceil(self.trip_length / constants_map["HOT_WARM_CLOTHES"][key]),
                        "checkbox": self.checkbox
                    }
                    self.packing_list.append(item_obj)
            elif COOL <= avg_temp < WARM:
                if value == "Clothes" and key in constants_map["WARM_COOL_CLOTHES"].keys():
                    item_obj = {
                        "item": key.capitalize(),
                        "category": value,
                        "count": ceil(laundry_trip_length / constants_map["WARM_COOL_CLOTHES"][key]) if self.laundry == 'Yes' 
                        else ceil(self.trip_length / constants_map["WARM_COOL_CLOTHES"][key]),
                        "checkbox": self.checkbox
                    }
                    self.packing_list.append(item_obj)
            elif CHILLY <= avg_temp < COOL:
                if value == "Clothes" and key in constants_map["COOL_CHILLY_CLOTHES"].keys():
                    item_obj = {
                        "item": key.capitalize(),
                        "category": value,
                        "count": ceil(laundry_trip_length / constants_map["COOL_CHILLY_CLOTHES"][key]) if self.laundry == 'Yes' 
                        else ceil(self.trip_length / constants_map["COOL_CHILLY_CLOTHES"][key]),
                        "checkbox": self.checkbox
                    }
                    self.packing_list.append(item_obj)
            elif avg_temp < CHILLY:
                if value == "Clothes" and key in constants_map["COLD_CLOTHES"].keys():
                    item_obj = {
                        "item": key.capitalize(),
                        "category": value,
                        "count": ceil(laundry_trip_length / constants_map["COLD_CLOTHES"][key]) if self.laundry == 'Yes' 
                        else ceil(self.trip_length / constants_map["COLD_CLOTHES"][key]),
                        "checkbox": self.checkbox
                    }
                    self.packing_list.append(item_obj)

    def create_list(self):
        items_dict = self.create_items_dict()
        self.non_clothes_items(items_dict)
        self.non_count_clothes(items_dict)
        self.regular_clothes(items_dict)
        return self.packing_list
