import datetime

from flask import Blueprint, request, jsonify

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



