FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python2.7
RUN apt-get install -y python-dev python-setuptools python-pip
RUN pip install -U pip
RUN pip install django==1.8.3
ADD . /www-data/
EXPOSE 8000
CMD ['/usr/bin/python2.7', '/www-data/manage.py', 'runserver', '127.0.0.1:8000']
