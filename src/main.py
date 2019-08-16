#!/usr/bin/env python
from datetime import datetime
from utils import get_weather, get_trip_details, write_packing_list, send_email
from os.path import join as path_join


if __name__ == "__main__":
    destination = get_trip_details.destination
    travel_guide = get_trip_details.travel_guide
    item_list = get_trip_details.item_list.replace(".csv", "")

    year = datetime.today().year
    month = datetime.today().month

    output_file = destination + '_' + item_list + '_' + str(year) + '_packing.txt'
    output_path = path_join("trips", output_file)

    weather = get_weather.GetWeather(get_trip_details)
    weather_details = weather.query_api()

    final_list = write_packing_list.WriteItems(get_trip_details, output_path, year, month, weather_details)
    final_list.write_list()

    if travel_guide.lower() == 'yes':
        import pdfkit
        pdfkit.from_url('http://wikitravel.org/en/' + get_trip_details.destination_underscore,
                        destination + '_Travel_Guide' + '.pdf')

    send_email.send_email(output_path)
