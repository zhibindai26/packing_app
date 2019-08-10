import requests


class GetWeather:
    def __init__(self, city, trip_length, international):
        self.international = international.lower()
        self.trip_length = trip_length
        self.api_key = "&key=5857cc9ae47b48278e8772d1ca50caa2"
        self.units = "&units=I"
        self.base_url = "https://api.weatherbit.io/v2.0/forecast/daily"
        if self.international == 'yes':
            self.world_cities_dict = self.get_intl_cities_dict
            self.search = "?city=" + city + "&country=" + self.world_cities_dict[city]
        else:
            self.us_cities_dict = self.get_us_cities_dict()
            self.search = "?city=" + city + "," + self.us_cities_dict[city]

        self.query_string = self.base_url + self.search + self.api_key + self.units

    @staticmethod
    def get_intl_cities_dict():
        world_cities = {}
        with open("csv\\world_cities.csv", "r") as infile:
            for line in infile:
                row = line.strip()
                row = row.split(',')
                city = row[0].strip()
                code = row[5].strip()
                world_cities[city] = code
        return world_cities

    @staticmethod
    def get_us_cities_dict():
        us_cities = {}
        with open("csv\\us_cities.csv", "r") as infile:
            for line in infile:
                row = line.strip()
                row = row.split(',')
                city = row[0].strip()
                state = row[1].strip()
                us_cities[city] = state
        return us_cities

    def query_api(self):
        r = requests.get(self.query_string)
        if r.status_code == 200:
            self.get_weather_details(r.json)
        else:
            print("API request failed")
        return r.status_code

    def get_weather_details(self, weather_data):
        # todo
        # parse returned weather data json

        avg_high_list = []
        avg_low_list = []
        precip_list = []
        conditions_list = []
        rain = False
        sunshine = False

        # calculate weather details
        delete_from_avgs = -(len(avg_high_list) - int(self.trip_length) - 1)

        if len(avg_high_list) > int(self.trip_length) and delete_from_avgs != 0:
            del avg_high_list[delete_from_avgs:]
            del avg_low_list[delete_from_avgs:]
            del precip_list[delete_from_avgs:]
            del conditions_list[delete_from_avgs:]

        avg_high = sum(avg_high_list) / float(len(avg_high_list))
        avg_low = sum(avg_low_list) / float(len(avg_low_list))
        avg_temp = (avg_low + avg_high) / 2

        if max(precip_list) >= 20:
            rain = True

        if "Partly Cloudy" in conditions_list or "Clear" in conditions_list:
            sunshine = True