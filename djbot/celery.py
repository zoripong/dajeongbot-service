from __future__ import absolute_import

from celery import Celery
from celery.schedules import crontab

from config import BROKER_URL, CELERY_RESULT_BACKEND
from .factory import create_app
#from flask import Flask
from djbot.models.models import db

# pip install eventlet
# celery -A djbot.tasks worker -l info -P eventlet

#flask_app = create_app()

app = Celery('djbot',                               # 첫번째 값은 현재 프로젝트의 이름을 설정하고
             broker=BROKER_URL,                      # broker: 브로커에 접속할 수 있는 URL을 설정.
             backend=CELERY_RESULT_BACKEND)
#db.init_app(app)
app.conf.update(
    BROKER_URL=BROKER_URL,
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE={
        'notification-every-minutes': {
            'task': 'djbot.tasks.register_calendar_notification',
            'schedule': crontab(minute='*/1'),      # 특정 시간 뿐만 아니라 특정 요일과 같은 다양한 단위시간 설정을 지원
        },
        'ask-every-minutes': {
            'task': 'djbot.tasks.register_calendar_question',
            'schedule': crontab(minute='*/1'),
        },
        'congratulate-every-day': {
            'task': 'djbot.tasks.congratulate_birthday',
            'schedule': crontab(minute=0, hour=0),
        },

    }
)
