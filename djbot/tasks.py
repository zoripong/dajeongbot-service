from __future__ import absolute_import

import datetime
import time

from djbot.celery import app
from djbot.controllers.notification import notify
from djbot.models.models import *

# [ Example ]
# @app.task
# def say_hello():          # 실제 백그라운드에서 작업할 내용을 task 로 정의한다.
#     print("Hello, celery!")


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
        user_datetime_object = time.strptime(account['notify_time'], '%H:%M')
        user_time = datetime.time(user_datetime_object[3], user_datetime_object[4]).strftime("%H:%M")
        now_time = datetime.datetime.now().strftime("%H:%M")

        if now_time > user_time:
            tokens = FcmToken.query.filter(FcmToken.account_id == event['account_id']).all
            title = "오늘 일정이 있어요!"
            message = event['schedule_where']+"에서 "+event['schedule_what']
            for token in tokens:
                notify(token['token'], title, message)

    # fcm 토큰
    # print("일정을 등록합니다.")


# 회원이 등록한 일정이 끝났을 때 일정에 대한 질문을 예약합니다.
@app.task
def register_calendar_question():
    print("일정을 등록합니다.")

    