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


@bp.route('/notifications')
def notification():
    push_service = FCMNotification(api_key=config.FCM_API)
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    events = Event.query \
        .filter(Event.review.is_(None), Event.schedule_when == today, Event.account_id == 32) \
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

    contents = ["오늘 하루 어땠니???"]

    param = {
        "title": "당신의 하루를 다정봇에게 들려주세요 :)",
        "message": "오늘 " + str(len(events)) + "개의 일정이 있습니다.",
        "data": {
            "status": "Success",
            "result": {
                "id": 32,
                "node_type": 2,
                "chat_type": 4,
                "time": str(int(time.time() * 1000)),
                "img_url": [],
                "content": contents,
                "events": event_json
            }
        }
    }
    for content in contents:
        chat = Chat(account_id=32, content=content, node_type=2,
                    chat_type=4, time=str(int(time.time() * 1000)), isBot=1, carousel_list=str(event_json))
        db.session.add(chat)
        db.session.commit()

    token = "e5_YzavRkOA:APA91bHZUwqG4jnOyd5awG74Pz3FjNgjyA1AzFQ2Ld41xYZBkWZFE3zJNYJ3Rt5eSE3J-an7IeZlCYPS4H7d_XvIOrDDe3oX8ATmMl40aXvGdMOOv8dgmsBYHaUlbKG28Wvzj_t9SCZz"
    push_service.notify_single_device(registration_id=token, data_message=param, content_available=True)

    return jsonify(param)

