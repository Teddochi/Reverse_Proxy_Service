port = 1235

# Threshold for response time 
slow_request_threshold = 5

nextbus_path =  'http://webservices.nextbus.com/service/publicXMLFeed'
not_found = 'https://designmodo.com/wp-content/uploads/2013/03/Saaspose.jpg'
stats_path = '/stats'
command_parameter = '?command='
proxy_url = 'http://localhost:' + str(port)
clean_data_file = {'slow_requests':{}, 'queries':{}}
clean_data_file_str = '{"slow_requests": {}, "queries": {}}'

