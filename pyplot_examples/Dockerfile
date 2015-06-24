FROM python:2-onbuild

RUN apt-get update
RUN apt-get install -y mongodb

RUN mkdir /data
RUN mkdir /data/db

CMD ["service mongod start"]