FROM python:3.7.3-slim-stretch

COPY ./Pipfile /opt/axolote/Pipfile

COPY ./Pipfile.lock /opt/axolote/Pipfile.lock

WORKDIR /opt/axolote

RUN pip install pipenv

RUN pipenv install --system --deploy
