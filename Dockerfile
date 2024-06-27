FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3

RUN mkdir /app

RUN apt update \
  && apt install -y cron \
  && pip3 install --upgrade pip \
  && pip3 install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /app/

WORKDIR /app

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
COPY ./hotel_management_system /app
WORKDIR /app

RUN touch logfile.log

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
