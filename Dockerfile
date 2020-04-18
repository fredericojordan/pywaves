FROM python:3.8-slim-buster

RUN apt-get update && apt-get install --yes libmagic-dev libproj-dev gdal-bin

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD requirements/base.txt ./requirements.txt
RUN  python -m pip install -U pip && pip install -r requirements.txt
COPY . /usr/src/app

CMD ["sh", "docker-entrypoint.sh"]
