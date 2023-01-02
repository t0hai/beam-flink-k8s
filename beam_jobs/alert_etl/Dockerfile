ARG PYTHON_VERSION=3.9
ARG BEAM_VERSION=2.43.0

FROM apache/beam_python${PYTHON_VERSION}_sdk:${BEAM_VERSION} AS base

FROM base AS poetry

ENV POETRY_VERSION=1.3.1

RUN pip3 install "poetry==$POETRY_VERSION"

WORKDIR /src

# Generate requirements.txt
COPY pyproject.toml poetry.lock /src/
RUN poetry export --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt

FROM base as production

COPY --from=poetry /src/requirements.txt  /tmp/requirements.txt
RUN  pip3 install -r /tmp/requirements.txt

WORKDIR /src

COPY src/ /src/
