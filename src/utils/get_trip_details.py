import json

trip_config_json = "config\\trip_details.json"
email_config_json = "config\\email_config.json"


def json_to_dict(json_file):
    with open(json_file) as j:
        return json.load(j)


trip_config_dict = json_to_dict(trip_config_json)
destination = trip_config_dict["destination"]
destination_underscore = destination.replace(' ', '_')
trip_length = float(trip_config_dict["days"])
laundry = trip_config_dict["laundry"].upper()
nice_clothes = trip_config_dict["nice_clothes"].upper()
international = trip_config_dict["international"]
item_list = trip_config_dict["item_list"]
swimming = trip_config_dict["swimming"]
email_recipient = trip_config_dict["email_recipient"]

email_config = json_to_dict(email_config_json)
email_user = email_config["email_user"]
email_password = email_config["email_password"]