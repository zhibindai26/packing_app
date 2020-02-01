import get_weather, create_packing_list, constants

def get_packing_list(event, context):
    weather = get_weather.GetWeather(event)
    weather_details = weather.query_api()

    final_list = create_packing_list.WriteItems(event, weather_details)
    packing_list = final_list.create_list()
    
    response_obj = {}
    response_obj['statusCode'] = 200
    response_obj['body'] = packing_list
    return response_obj
