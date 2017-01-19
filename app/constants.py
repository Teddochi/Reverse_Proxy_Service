port = 1235

# Threshold for response time 
slow_request_threshold = .5

nextbus_url =  'http://webservices.nextbus.com/service/publicXMLFeed'
stats_path = '/stats'
database_path = 'app/database/'
command_parameter = '?command='
proxy_url = 'http://localhost:' + str(port)
clean_stats_file = {'slow_requests':{}, 'queries':{}}
