import datetime

from celery import Celery

import config

from pyfcm import FCMNotification
from djbot.models.models import *

#   #   #   #   #   #
#  일정 등록 컨트롤러 #
#   #   #   #   #   #


push_service = FCMNotification(api_key=config.FCM_API)


def register_event(reply, content):
    current = datetime.datetime.now()
    param = reply['responseSet']['result']['parameters']
    message_result = reply['responseSet']['result']['result']
    when = current + datetime.timedelta(days=int(param['when']))
    when = when.strftime('%Y-%m-%d')
    event = Event(account_id=content['account_id'], schedule_when=when, schedule_where=param['where'],
                  schedule_what=param['what'], assign_time=message_result[0]['timestamp'],
                  detail=param['detail'])
    db.session.add(event)

    # TODO : FCM alarm 예약
    # FCM -> 일정 후기 & 일정 안내


def notify():
    registration_id = "ecEigPKJXf0:APA91bFWZkgS-tNpXnQ9Ea0TEASr0EXTiyOGhYoMbtgn75TrR2Y3TF2KbDx1SbkdovEdBuibp262SiVFCjwIPJAWQNg9kKlOx4MaurbpIxVVYaSpa5vJylZKidbieoyMEU53R5brmLQz"
    message_title = "Uber update"
    message_body = "Hi john, your customized news for today is ready"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    return result