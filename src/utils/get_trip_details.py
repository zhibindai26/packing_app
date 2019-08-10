from ConfigParser import ConfigParser

config = ConfigParser()
config.read('trip_details.ini')
destination = config.get('main', 'destination')
destination_underscore = destination.replace(' ', '_')
trip_length = float(config.get('main', 'days'))
laundry = config.get('main', 'laundry').upper()
nice_clothes = config.get('main', 'nice_clothes').upper()
email_config = ConfigParser()
email_config.read('email_config.ini')
international = config.get('main', 'international')