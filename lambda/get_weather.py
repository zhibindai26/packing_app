import requests


class GetWeather:
    def __init__(self, trip_details):
        self.city = trip_details["destination"].lower()
        self.international = trip_details["international"].capitalize()
        self.trip_length = int(trip_details["duration"]) + 1
        self.days = "&days=" + str(self.trip_length)
        self.api_key = "&key=" + trip_details["weather_api_key"]
        self.units = "&units=I"
        self.base_url = "https://api.weatherbit.io/v2.0/forecast/daily"
        
        if self.international == 'Yes':
            self.country_code = self.get_intl_ctry_code(self.city)
            self.search = "?city=" + self.city + "&country=" + self.country_code
        else:
            self.search = "?city=" + self.city

        self.query_string = self.base_url + self.search + self.api_key + self.units + self.days

    @staticmethod
    def get_intl_ctry_code(city_to_search):
        with open("./csv/world_cities.csv", "r") as infile:
            for line in infile:
                row = line.strip().split(',')
                city = row[0].strip().lower()
                if city == city_to_search:
                    return row[5].strip()

    def query_api(self):
        r = requests.get(self.query_string)
        if r.status_code == 200:
            return self.get_weather_details(r.json())
        else:
            print("API request failed")
            return r.status_code

    def get_weather_details(self, weather_data):
        avg_high_list = [int(round(x["max_temp"])) for x in weather_data["data"]]
        avg_low_list = [int(round(x["min_temp"])) for x in weather_data["data"]]
        precip_list = [x["pop"] for x in weather_data["data"]]
        if self.trip_length > 4 or max(precip_list) >= 20:
            rain = True
        else:
            rain = False

        # calculate weather details
        avg_high = sum(avg_high_list) / float(len(avg_high_list))
        avg_low = sum(avg_low_list) / float(len(avg_low_list))
        avg_temp = (avg_low + avg_high) / 2

        return {
            "city": weather_data["city_name"],
            "timezone": weather_data["timezone"],
            "country_code": weather_data["country_code"],
            "state_code": weather_data["state_code"],
            "rain": rain,
            "avg_high": round(avg_high),
            "avg_low": round(avg_low),
            "avg_temp": round(avg_temp)
        }
