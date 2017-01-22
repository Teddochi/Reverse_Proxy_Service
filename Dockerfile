FROM python:2.7

ENV PYTHONUNBUFFERED=1

EXPOSE 8888
WORKDIR /usr/src/app

# Copy the application 
COPY . /usr/src/app

RUN pip install requests
RUN pip install expiringdict
RUN pip install mysql-connector

CMD ["./Run.sh"]