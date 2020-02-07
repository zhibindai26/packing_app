import json
import get_weather, create_packing_list, constants


def get_packing_list(event, context):
    weather = get_weather.GetWeather(event)
    weather_details = weather.query_api()

    final_list = create_packing_list.WriteItems(event, weather_details)
    packing_list = final_list.create_list()

    response_obj = {
        "status_code": 200,
        "city": weather_details["city"],
        "timezone": weather_details["timezone"],
        "country_code": weather_details["country_code"],
        "state_code": weather_details["state_code"],
        "avg_temp": weather_details["avg_temp"],
        "avg_high": weather_details["avg_high"],
        "avg_low": weather_details["avg_low"],
        "body": packing_list
    }
    return response_obj
