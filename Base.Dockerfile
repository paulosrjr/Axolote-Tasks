FROM python:3.7.3-slim-stretch

COPY ./Pipfile /opt/axolote/Pipfile

COPY ./Pipfile.lock /opt/axolote/Pipfile.lock

WORKDIR /opt/axolote

RUN apt-get update && \
    apt-get -s dist-upgrade | grep "^Inst" | grep -i securi | awk -F " " {'print $2'} | xargs apt-get install -y

RUN apt-get update && \
    apt-get install sshpass rsync openssh-client rssh -y && \
    apt-get clean

RUN pip install pipenv

RUN pipenv install --system --deploy

