from ConfigParser import ConfigParser


config = ConfigParser()
config.read('config\\trip_details.ini')
destination = config.get('main', 'destination')
destination_underscore = destination.replace(' ', '_')
trip_length = float(config.get('main', 'days'))
laundry = config.get('main', 'laundry').upper()
nice_clothes = config.get('main', 'nice_clothes').upper()
email_config = ConfigParser()
email_config.read('config\\email_config.ini')
international = config.get('main', 'international')
item_list = config.get('main', 'item_list')
swimming = config.get('main', 'swimming')
travel_guide = config.get('main', 'travel_guide')
