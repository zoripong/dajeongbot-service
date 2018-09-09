import datetime

from celery import Celery

import config

from pyfcm import FCMNotification
from djbot.models.models import *

#   #   #   #   #   #
#  일정 등록 컨트롤러 #
#   #   #   #   #   #


push_service = FCMNotification(api_key=config.FCM_API)


def register_event(reply, content, id):
    current = datetime.datetime.now()
    param = reply['responseSet']['result']['parameters']
    message_result = reply['responseSet']['result']['result']
    when = current + datetime.timedelta(days=int(param['when']))
    when = when.strftime('%Y-%m-%d')

    print('여기보세요~')
    print(content)

    event = Event(account_id=id, schedule_when=when, schedule_where=param['where'],
                  schedule_what=param['what'], assign_time=message_result[0]['timestamp'],
                  detail=param['detail_content'])
    db.session.add(event)

