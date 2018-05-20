import urllib2
import json
import get_trip_details

us_cities = {}
def create_US_cities_dict():
    with open("csv\us_cities.csv", "r") as infile:
        for line in infile:
            row = line.strip()
            row = row.split(',')
            city = row[0].strip()
            state = row[1].strip()
            us_cities[city] = state

create_US_cities_dict()

avg_high_list = []
avg_low_list = []
precip_list = []
conditions_list = []

f = urllib2.urlopen('http://api.wunderground.com/api/cacea4c99bc7010d/forecast10day/conditions/q/%s/%s.json' %
                    (us_cities[get_trip_details.destination], get_trip_details.destination_underscore))
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


# calculate weather details
delete_from_avgs = -(len(avg_high_list) - int(get_trip_details.trip_length) - 1)

if len(avg_high_list) > int(get_trip_details.trip_length) and delete_from_avgs != 0:
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