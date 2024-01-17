# pull official base image
FROM python:3.10.13-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt

# install dependencies
RUN set -eux
RUN apk add --no-cache --virtual .build-deps build-base \
    libressl-dev libffi-dev gcc musl-dev python3-dev
RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

# copy project
COPY . /usr/src/app/