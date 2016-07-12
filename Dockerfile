FROM ubuntu:16.04
RUN sed -i 's/archive/cn.archive/g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y python2.7
RUN apt-get install -y python-dev python-pip
RUN pip install update
ADD . /www-data/
EXPOSE 8000
CMD ['/usr/bin/python2.7', '/www-data/manage.py', 'runserver', '127.0.0.1:8000']