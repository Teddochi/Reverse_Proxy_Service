FROM ubuntu:latest

MAINTAINER Ted Ochiai

# Install required tools
RUN apt-get update && apt-get install -y \
git \
python \
python-distribute \
python-pip

# Update pip
RUN pip install --upgrade pip

# Install Twisted Matrix
RUN pip install Twisted