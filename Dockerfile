FROM ubuntu

MAINTAINER Ted Ochiai

RUN apt-get update

RUN apt-get install -y git

# Python specific tools}
RUN apt-get install -y python python-dev python-distribute python-pip

# Install requirements
RUN pip install --upgrade pip
RUN pip install Twisted