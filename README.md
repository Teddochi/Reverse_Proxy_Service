# Reverse_Proxy_Service
This is the repository for my reverse-proxy service for the NextBus public transportation feed.  
This service was created for a coding challenge assigned by the ThousandEyes recruitment team.

## Assumptions
Due to the way that Docker runs on different machines, this repository is set up under the assumption that you are using a Linux machine.  There are guidelines below to adjust the application for other types of machines in case your container is running on a virtual machine. The main difference is that the server will be hosted on your docker-machine ip instead of localhost.  

## Requirements
- Docker

## Usage
To start the reverse proxy server, use:
```
./Run.sh
```
This will use Docker to run the server at http://localhost:8888 on your machine.

If you are running the server on a virtual machine, connect to the server at the IP of your docker machine.
You can find this IP with the following command:
```
docker-machine ip
```

To stop the server, use:
```
./Stop.sh
```
Documentation on the NextBus Public XML Feed can be found here: http://www.nextbus.com/xmlFeedDocs/NextBusXMLFeed.pdf
To use this reverse proxy, enter nextbus commands like so:
- http://localhost:8888/agencyList
- http://localhost:8888/routeList&a=sf-muni

You can also access the statistics of the database through the stats endpoint.
- http://localhost:8888/stats

This application was designed to have several configurable settings. 
You can make changes to "app/constants.py" to adjust the following settings:
- Server port (You will also need to adjust the Dockerfile and docker-compose.yml to reflect any changes here)
- Maximum cached elements
- Time limit for cached items
- Threshold for defining slow response times

## Implementation details
The application code can be found in the "app" directory.  
- "app.py": starts the server and defines the handler for all requests
- "tools.py": defines several functions used by the handler
- "constants.py": defines some constants used throughout the application
- "clean_db.py": can be used to reset the database if desired

A testing suite can be found in the "testing" directory.
- "test_driver.py": runs all of the unit tests created for this application
- "context.py": imports constants from the application for testing

Application scripts
- "Run.sh": executes the application using Docker-Compose
- "Stop.sh": stops the application
- "Tests.sh": runs unit tests against the running application
- "Clean_Database.sh": resets the database if desired.  You should restart the server if you do so.  
- "Docker_Run.sh": This script is used in the Dockerfile to start the application

Database
- This application connects to a MySQL database hosted by https://www.freemysqlhosting.net/
- Statistics information is stored in this database

## Testing
This project includes a testing suite that you can run using:
```
./Tests.sh
```

If you are running the server on a virtual machine, find the IP address of your virtual machine with:
```
docker-machine ip
```
You will need to edit "testing/test_driver.py" to connect to this URL instead of localhost.  