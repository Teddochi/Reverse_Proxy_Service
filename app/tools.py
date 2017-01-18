import constants

# Route the user to the proper nextbus api endpoint according to path
def handlePath(path):
	if path == constants.stats_path:
		return constants.not_found
	elif path:
		# A command was entered. 
		return constants.nextbus_path + constants.command_parameter + path
	else:
		# Direct user to publicXMLFeed of nextbus
		return constants.nextbus_path