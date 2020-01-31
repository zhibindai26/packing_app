#!/usr/bin/env python
from datetime import datetime
from utils import get_weather, get_trip_details, write_packing_list
from os.path import join as path_join


if __name__ == "__main__":
    destination = get_trip_details.destination
    item_list = get_trip_details.item_list.replace(".csv", "")

    year = datetime.today().year
    month = datetime.now().strftime("%B")
    underscore = "_"
    packing = "_packing.txt"

    output_file = destination + underscore + item_list + underscore + str(year) + packing
    output_path = path_join("trips", output_file)

    weather = get_weather.GetWeather(get_trip_details)
    weather_details = weather.query_api()

    final_list = write_packing_list.WriteItems(get_trip_details, output_path, year, month, weather_details)
    final_list.write_list()
