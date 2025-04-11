FROM python:3.11.1-slim-bullseye

WORKDIR /app

COPY ./ ./

RUN apt-get update \
  && apt-get upgrade -y \
  && pip install -U pip \
  && pip install poetry \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app
ENV LANG ja_JP.UTF-8