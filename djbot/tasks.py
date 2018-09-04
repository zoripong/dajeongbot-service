from __future__ import absolute_import

import datetime
import time

from pyfcm import FCMNotification

import config
from djbot.celery import app
from djbot.models.models import *

# [ Example ]
# @app.task
# def say_hello():          # 실제 백그라운드에서 작업할 내용을 task 로 정의한다.
#     print("Hello, celery!")

push_service = FCMNotification(api_key=config.FCM_API)


# 회원이 등록한 일정의 시작 시간에 안내를 할 수 있도록 메세지를 예약합니다.
@app.task
def register_calendar_notification():
    # 이벤트 목록 (send is 0)
    # 이벤트에 대한 정보와 회원 account_id
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    events = Event.query.filter(Event.send == 0, Event.schedule_when == today).order_by(Event.id).all()
    for event in events:
        # 해당 이벤트를 등록한 계정의 알림 설정 시간과 현재시간을 비교
        account = Account.query.filter(Account.id == event['account_id'])
        title = "오늘 일정이 있어요!"
        message = event['schedule_where'] + "에서 " + event['schedule_what']
        send_fcm_message(account['notify_time'], event['account_id'], title, message)
        # TODO : send update


# 회원이 등록한 일정이 끝났을 때 일정에 대한 질문을 예약합니다.
@app.task
def register_calendar_question():
    # 오늘 일어난 event 중 후기가 null 이면서 사용자의 일기쓰는 시간이 지난 경우
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    events = Event.query.filter(Event.review.is_(None), Event.schedule_when == today).order_by(Event.id).all()

    for event in events:
        account = Account.query.filter(Account.id == event['account_id'])
        title = "당신의 하루를 다정봇에게 들려주세요 :)"
        message = event['schedule_where'] + "에서 " + event['schedule_what']
        send_fcm_message(account['ask_time'], event['account_id'], title, message)
        # TODO : review update


# 시간을 비교하여 사용자의 기기에 fcm 알림을 보냅니다.
# param : 비교 시간, 계정 식별번호, 알림 제목, 알림 내용
def send_fcm_message(check_time, account_id, title, message):

    user_datetime_object = time.strptime(check_time, '%H:%M')
    user_time = datetime.time(user_datetime_object[3], user_datetime_object[4]).strftime("%H:%M")
    now_time = datetime.datetime.now().strftime("%H:%M")

    if now_time > user_time:
        tokens = FcmToken.query.filter(FcmToken.account_id == account_id).all
        for token in tokens:
            # send the fcm notification
            push_service.notify_single_device(registration_id=token['token'], message_title=title, message_body=message)