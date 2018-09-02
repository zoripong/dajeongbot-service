from __future__ import absolute_import

from celery import Celery
from celery.schedules import crontab

from config import BROKER_URL, CELERY_RESULT_BACKEND

# pip install eventlet
# celery -A <module> worker -l info -P eventlet


app = Celery('djbot',                               # 첫번째 값은 현재 프로젝트의 이름을 설정하고
             broker=BROKER_URL,                      # broker: 브로커에 접속할 수 있는 URL을 설정.
             backend=CELERY_RESULT_BACKEND)


app.conf.update(
    BROKER_URL=BROKER_URL,
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE={
        'say_hello-every-seconds': {
            'task': 'djbot.tasks.say_hello',
            'schedule': crontab(hour='*', minute='*'),      # 특정 시간 뿐만 아니라 특정 요일과 같은 다양한 단위시간 설정을 지원
            'args': ()
        }
    }
)
