FROM python:3.7.3-slim-stretch

COPY . /opt/axolote

WORKDIR /opt/axolote

RUN pip install pipenv

RUN pipenv install --system --deploy
