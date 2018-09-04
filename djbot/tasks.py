from __future__ import absolute_import

import datetime
import time

from djbot.celery import app
from djbot.models.models import *

# [ Example ]
# @app.task
# def say_hello():          # 실제 백그라운드에서 작업할 내용을 task로 정의한다.
#     print("Hello, celery!")


# 회원이 등록한 일정의 시작 시간에 안내를 할 수 있도록 메세지를 예약합니다.
@app.task
def register_calendar_notification():
    # 이벤트 목록 (send is 0)
    # 이벤트에 대한 정보와 회원 account_id
    events = Event.query.filter(Event.send == 0).order_by(Event.id).all()       # TODO : 오늘 날짜!
    for event in events:
        # 회원이 설정한 시간 (아침)보다 늦었으면 fcm 토큰 전송
        now_time = datetime.datetime.now().strftime("%H:%M")

        #if now_time > user
        user_notify_time = '08:00'
        datetime_object = time.strptime(user_notify_time, '%H:%M')
        user = datetime.time(datetime_object[3], datetime_object[4]).strftime("%H:%M")

        account = Account.query.filter(id == event['account_id'])
        account['notify_time']
    # fcm 토큰
    print("일정을 등록합니다.")


# 회원이 등록한 일정이 끝났을 때 일정에 대한 질문을 예약합니다.
@app.task
def register_calendar_question():
    print("일정을 등록합니다.")