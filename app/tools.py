import constants

# Route the user to the proper nextbus api endpoint according to path
def getNextBusUrl(path):
	if path == "/":
		return constants.nextbus_path 
	else:
		return constants.nextbus_path + constants.command_parameter + path[1:]


def get_ip_file_name(self):
	return self.client_address[0].replace(".", "-") + ".json"