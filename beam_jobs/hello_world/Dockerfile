ARG PYTHON_VERSION=3.9

FROM --platform=linux/amd64 python:${PYTHON_VERSION}-slim-bullseye AS base

COPY ./requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

WORKDIR /src

COPY src/ /src/
