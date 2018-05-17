#!/bin/bash

#celery -A actions worker -E -l debug
celery worker --app actions --config celeryconfig.py -E -n 1.%h --loglevel=info
#celery worker --app actions -E -n 1.%h --loglevel=info
