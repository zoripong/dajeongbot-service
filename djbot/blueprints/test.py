import datetime
import time

from flask import Blueprint, request, jsonify
from pyfcm import FCMNotification

import config
from djbot.controllers import schedule
from djbot.models.models import *


bp = Blueprint('test', __name__)


@bp.route("/")
def hello_world():
    # current = datetime.datetime.now()
    # tomorrow = current + datetime.timedelta(days=6)
    # print(tomorrow)
    return 'hello world'


@bp.route("/register")
def register():
    user = Account(user_id="test2", name="test2", birthday="2000.05.09.", account_type=1, bot_type=1)
    db.session.add(user)
    db.session.commit()

    return 'hello world'


@bp.route("/join")
def join():
    user_id = 'test'
    password = 'test'
    account = Account.query.join(CustomAccount, Account.id == CustomAccount.account_id) \
        .add_columns(Account.id, Account.user_id, CustomAccount.password) \
        .filter(Account.user_id == user_id, CustomAccount.password == password) \
        .all()

    if len(account) == 1:
        return "Success"
    else:
        return "Failed"


@bp.route("/json", methods=['POST'])
def json22():
    content = request.get_json(force=True)
    # if "id" in content['response']:
    #     print("hi")
    # else:
    #     print("hello")
    print(content)
    return jsonify(content)


@bp.route("/none")
def is_none():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    events = Event.query.filter(Event.review.is_(None), Event.schedule_when == today).order_by(Event.id).all()
    return jsonify([{
        "id": event.id,
        "schedule_when": event.schedule_when,
        "schedule_where": event.schedule_where,
        "schedule_what": event.schedule_what,
        "assign_time": event.assign_time,
        "detail": event.detail,
        "review": event.review
    } for event in events])


push_service = FCMNotification(api_key=config.FCM_API)


@bp.route('/notifications')
def notification():
    # 이벤트 목록 (send is 0)
    # 이벤트에 대한 정보와 회원 account_id
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    print(today)
    events = Event.query.filter(Event.notification_send == 0, Event.schedule_when == today).order_by(Event.id).all()
    print(len(today))

    for event in events:
        # 해당 이벤트를 등록한 계정의 알림 설정 시간과 현재시간을 비교
        accounts = Account.query.filter(Account.id == event.account_id).all()

        contents = ["오늘은 일정이 있는 날이네!",
                    event.schedule_where + "에서 " + event.schedule_what,
                    "오늘도 화이팅!"]
        param = {
            "title": "오늘 일정이 있어요!",
            "message": event.schedule_where + "에서 " + event.schedule_what,
            "data": {
                "status": "Success",
                "result": {
                    "node_type": 0,
                    "id": event.account_id,
                    "chat_type": 3,
                    "time": str(int(time.time() * 1000)),
                    "img_url": [],
                    "content": contents
                }
            }
        }
        print(param)
        for account in accounts:
            # 해당 일정에 대해 안내 하였음을 업데이트 함
            if send_fcm_message(account.notify_time, event.account_id, 3, contents, param):
                event.notification_send = 1
    db.session.commit()
    return jsonify({"result": "ok"})


@bp.route('/ask')
def ask():
    # 오늘 일어난 event 중 후기가 null 이면서 사용자의 일기쓰는 시간이 지난 경우
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    accounts = Account.query.all()
    for account in accounts:
        events = Event.query \
            .filter(Event.review.is_(None), Event.schedule_when == today, Event.account_id == account.id) \
            .order_by(Event.id).all()

        event_json = []
        for event in events:
            event_json.append({
                "id": event.id,
                "account_id": event.account_id,
                "schedule_when": event.schedule_when,
                "schedule_where": event.schedule_where,
                "schedule_what": event.schedule_what,
                "assign_time": event.assign_time,
                "detail": event.detail,
                "review": event.review,
                "notification_send": event.notification_send,
                "question_send": event.question_send
            })

        content = ["오늘 하루 어땠니?"]
        param = {
            "title": "당신의 하루를 다정봇에게 들려주세요 :)",
            "message": "오늘 " + str(len(events)) + "개의 일정이 있습니다.",
            "data": {
                "status": "Success",
                "result": {
                    "id": account.id,
                    "node_type": 1,
                    "chat_type": 5,
                    "time": str(int(time.time() * 1000)),
                    "img_url": [],
                    "content": content,
                    "events": event_json
                }
            }
        }

        # 해당 일정에 대해 안내 하였음을 업데이트 함
        if send_fcm_message(account.ask_time, account.id, 5, content, param):
            for event in events:
                event.question_send = 1

        db.session.commit()
    return jsonify({"result": "ok"})


# 시간을 비교하여 사용자의 기기에 fcm 알림을 보냅니다.
# param : 비교 시간, 계정 식별번호, 알림 제목, 알림 내용
def send_fcm_message(check_time, account_id, chat_type, contents, param):
    user_datetime_object = time.strptime(check_time, '%H:%M')
    user_time = datetime.time(user_datetime_object[3], user_datetime_object[4]).strftime("%H:%M")
    now_time = datetime.datetime.now().strftime("%H:%M")

    if now_time > user_time:
        if chat_type == 4:
            for content in contents:
                chat = Chat(account_id=account_id, content=content, node_type=0,
                            chat_type=chat_type, time=str(int(time.time() * 1000)), isBot=1)
                db.session.add(chat)
        elif chat_type == 5:
            for content in contents:
                chat = Chat(account_id=account_id, content=content, node_type=1,
                            chat_type=chat_type, time=str(int(time.time() * 1000)), isBot=1,
                            slot_list=str(param['data']['result']['events']))
                db.session.add(chat)

        db.session.commit()
        tokens = FcmToken.query.filter(FcmToken.account_id == account_id).all()
        for token in tokens:
            # send the fcm notification
            print("메세지 전송 얍!")
            push_service.notify_single_device(registration_id=token.token, data_message=param, content_available=True)

        return True
    return False
