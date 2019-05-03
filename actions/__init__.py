from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
from fluent import sender

logger = sender.FluentSender('axolote', host='elasticsearch.infra.geofusion', port=21232)

def test_none(var_to_test):
    if var_to_test is None:
        raise ValueError('None variable')
        return False
    else:
        return True

try:
    celery_app = Celery('actions')
    celery_app.config_from_object('celeryconfig')
    celery_app.conf.update(
        result_expires=3600,
    )
except Exception as e:
    logger.emit('exception', {'description': 'celery instance', 'log': str(e)})
else:
    if __name__ == '__main__':
        celery_app.start()