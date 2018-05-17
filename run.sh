#!/bin/bash

celery worker --app actions --config celeryconfig.py -E -n 1.%h --loglevel=info
