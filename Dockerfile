FROM python:3.6-alpine
ADD . /opt/axolote
WORKDIR /opt/axolote
RUN pip install -r requirements.pip
CMD ["celery", "worker", "--app", "actions", "--config", "celeryconfig.py", "-E", "-n", "1.%h", "--loglevel=info"]
