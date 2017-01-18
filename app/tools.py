
nextbus_path =  'http://webservices.nextbus.com/service/publicXMLFeed?command='
not_found = "https://designmodo.com/wp-content/uploads/2013/03/Saaspose.jpg"
# Route the user to the proper nextbus api endpoint according to path
def handlePath(path):
	if path == '/stats':
		return not_found
	elif path == '/':
		return not_found
	else:
		return nextbus_path + path
	

