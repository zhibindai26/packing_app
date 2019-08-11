#!/usr/bin/env python
from datetime import datetime
from utils import get_weather, get_trip_details, write_packing_list, send_email

if __name__ == "__main__":

    from os.path import join as path_join

    destination = get_trip_details.destination
    trip_length = get_trip_details.trip_length
    international = get_trip_details.international
    travel_guide = get_trip_details.travel_guide

    output_file = destination + '_' + str(datetime.today().year) + '_packing.txt'
    output_path = path_join("trips", output_file)
    checkbox = '[   ] '

    weather = get_weather.GetWeather(destination, trip_length, international)
    weather_details = weather.query_api()

    with open(output_path, 'w') as outfile:
        outfile.write('Packing List For ' + str(datetime.now().strftime("%B")) + ' '
                      + str(datetime.today().year) + ' ' + destination.upper() + ' Trip')
        outfile.write('\n')
        outfile.write(str(int(trip_length)) + ' Days' + ' | ' +
                      'Temps: Avg High: ' + str(weather_details["avg_high"]) + ', ' + 'Avg Low: '
                      + str(weather_details["avg_low"]))
        outfile.write('\n')
        outfile.write('\n')

    final_list = write_packing_list.WriteItems(get_trip_details, output_path, weather_details)
    final_list.write_list()

    if travel_guide.lower() == 'yes':
        import pdfkit
        pdfkit.from_url('http://wikitravel.org/en/' + get_trip_details.destination_underscore,
                        destination + '_Travel_Guide' + '.pdf')

    send_email.send_email(output_path)
