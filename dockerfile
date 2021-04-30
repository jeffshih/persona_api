FROM python:3.8.6-slim-buster
MAINTAINER jeffshih <jeffhfs1224@gmail.com>
RUN apt-get update && apt-get install -y\
         libpq-dev\
         build-essential
EXPOSE 5000
WORKDIR /persona_api
COPY . .
RUN pip install -r requirements.txt
CMD python src/main.py