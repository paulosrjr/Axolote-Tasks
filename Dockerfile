FROM axolote/python-base-tasks:latest

COPY . /opt/axolote

WORKDIR /opt/axolote

RUN pipenv install --system --deploy

ENV C_FORCE_ROOT="true"

CMD ["celery", "worker", "--app", "actions", "--config", "celeryconfig.py", "-E", "-n", "1.%h", "--loglevel=info"]
