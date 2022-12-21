ARG PYTHON_VERSION=3.9
ARG BEAM_VERSION=2.43.0

FROM --platform=linux/amd64 apache/beam_python${PYTHON_VERSION}_sdk:${BEAM_VERSION} AS base

FROM base as production

WORKDIR /src

COPY ./requirements.txt  /tmp/requirements.txt
RUN  pip3 install -r /tmp/requirements.txt
