# The builder image, used to build the virtual environment
FROM python:3.11-slim-bookworm

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_HOME='/usr/local'

RUN pip install poetry==1.8.5

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY README.md pyproject.toml poetry.lock /code/
COPY pcba_helper/ /code/pcba_helper

ARG DEPENDENCY_GROUP

ENV DEPENDENCY_GROUP=${DEPENDENCY_GROUP}

RUN poetry install \
    $(test -n "$DEPENDENCY_GROUP" && echo "--only=$DEPENDENCY_GROUP") \
    --no-interaction \
    --no-ansi && rm -rf $POETRY_CACHE_DIR
