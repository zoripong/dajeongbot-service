import datetime

from flask import Blueprint, request, jsonify

from djbot.models.models import *
import json
import djbot.blueprints.danbee as danbee
import calendar
import time
import config

bp = Blueprint('api', __name__, url_prefix='/apis')

# test code


@bp.route("/")
def hello_world():
    current = datetime.datetime.now()
    tomorrow = current + datetime.timedelta(days=6)
    print(tomorrow)
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


# end of test code

# start of auth code
@bp.route('/users/<int:account_type>/<string:user_id>/<string:password>')
def login(account_type, user_id, password):

    j1 = [{
        "status": "Failed",
    }]
    if account_type == 0:
        # print(str(account_type) + "/" + user_id + "/" + password)
        account = CustomAccount.query.filter(CustomAccount.user_id == user_id, CustomAccount.password == password,
                                             CustomAccount.account_type == account_type).all()
        print(len(account))
        if len(account) == 1:
            j1 = [{
                "status": "OK",
                "user_info": {
                    "id": account[0].id,
                    "bot_type": account[0].bot_type,
                    "chat_session": "preparing"
                }
            }]
        elif len(account) < 1:
            j1 = [{
                "status": "NOT EXIST",
            }]
    else:
        # TODO: 토큰이 유효한지 체크!
        # 있는지 체크하고 있으면 업데이트 없으면 그냥 리턴
        account = ApiAccount.query.filter(ApiAccount.user_id == user_id, ApiAccount.account_type == account_type).all()
        if len(account) == 1:
            if account[0].token != password:
                # 토큰이 바뀌었다면 업데이트
                new_account = ApiAccount(user_id=account[0].user_id, name=account[0].name,
                                         birthday=account[0].birthday, account_type=account[0].account_type,
                                         bot_type=account[0].bot_type, token=password)
                db.session.delete(account[0])
                db.session.add(new_account)
                db.session.commit()
            j1 = [{
                "status": "OK",
                "user_info": {
                    "id": account[0].id,
                    "bot_type": account[0].bot_type,
                    "chat_session": "preparing"
                }
            }]
        else:
            j1 = [{
                "status": "NEW_API_USER",
                "account_type": account_type,
                "token": password,
            }]

    # TODO: 성공했을 경우 SESSION
    return json.dumps(j1)


@bp.route('/signup', methods=['GET','POST'])
def signup():
    # content = request.get_json(force=True)
    print(request.data, type(request.data))
    jsonString = request.data.decode("utf-8")
    content2 = json.loads(jsonString)
    print(type(content2))
    content = content2
    # 존재하는 아이디인지 체크
    result = {
        "status": "Failed"
        # "id": content["user_id"]
    }
    # print(type(content['account_type']))
    account = Account.query.filter(Account.user_id == content['user_id'], Account.account_type == content['account_type']).all()
    if len(account) == 0:
        # 존재하지 않는 아이디라면 insert
        detail = ApiAccount(user_id=content['user_id'], name=content['name'], birthday=content['birthday'],
                            account_type=content['account_type'], bot_type=content['bot_type'], token=content['token'])

        if content['account_type'] == 0:
            detail = CustomAccount(user_id=content['user_id'], name=content['name'], birthday=content['birthday'],
                                   account_type=content['account_type'], bot_type=content['bot_type'],
                                   password=content['password'])
        db.session.add(detail)
        db.session.commit()
        new_account = Account.query.filter(Account.user_id == content['user_id'],
                                       Account.account_type == content['account_type']).all()
        result = {
            "status": "Success",
            "user_info": {
                "id": new_account[0].id,
                "user_id": new_account[0].user_id,
                "name": new_account[0].name,
                "birthday": str(new_account[0].birthday),
                "account_type": new_account[0].account_type,
                "bot_type": new_account[0].bot_type
            }
        }
        add_message_for_new_user(new_account[0].id)

    elif len(account) >= 1:
        result = {
            "status": "ExistUser"
            # "id": content["user_id"]
        }
    return json.dumps(result)


# end of auth code

# start of message code
@bp.route('/messages', methods=['POST'])
def add_messages():
    # 사용자가 새로운 메세지를 보냄
    content = request.get_json(force=True)

    result = jsonify({"status": "Failed"})

    chat = Chat(account_id=content['account_id'], content=content['content'], chat_type=content['chat_type'],
                time=content['time'], isBot=content['isBot'])
    db.session.add(chat)
    db.session.commit()

    # 챗봇이랑 대화 chat_type으로 분류
    if content['chat_type'] == 0 :
        result = reply_message(content)
    elif content['chat_type'] == 1:
        result = reply_message_for_memory(content)

    return result


def add_message_for_new_user(account_id):
    ts = calendar.timegm(time.gmtime())
    # TODO : 캐릭터 컨셉으로 변환
    content = '반가워요 무엇을 도와드릴까요?' 

    chat = Chat(account_id=account_id, content=content, chat_type=0, time=str(ts), isBot=1)
    db.session.add(chat)
    db.session.commit()
    print("반가워~")


# 챗봇이 답장을 주는 부분
def reply_message(content):
    current = datetime.datetime.now()
    # 챗봇
    reply = danbee.message(content['content'], content['response'])
    reply_result = reply['responseSet']['result']['result']

    for result in reply_result:
        # print(result['message'])
        bot_message = result['message']
        chat = Chat(account_id=content['account_id'], content=bot_message, chat_type=content['chat_type'],
                    time=content['time'], isBot=1)
        db.session.add(chat)

    # print("receive\n",reply)

    if reply['responseSet']['result']['ins_id'] == "" \
            and reply['responseSet']['result']['ref_intent_id'] == "":
        result = {
            "status": "Intent is not Found",
        }
    else:
        # TODO : TEST
        # TODO : DEBUG : result is empty
        # 일정 등록
        # node_id가 SpeakNode_1533084803517에서 Event 저장
        if reply['responseSet']['result']['node_id'] == "SpeakNode_1533084803517":
            param = reply['responseSet']['result']['parameters']
            message_result = reply['responseSet']['result']['result']
            when = current + datetime.timedelta(days=param['where'])
            event = Event(account_id=content['account_id'], schedule_when=param['when'], schedule_where=when,
                          schedule_what=param['what'], assign_time=message_result[0]['timestamp'],
                          detail=param['detail'])
            db.session.add(event)
            # TODO : FCM alarm 예약

        elif reply['responseSet']['result']['node_id'] == "SpeakNode_1533088132355":
            # TODO: 지난 추억 가져오기
            num_date = reply['responseSet']['result']['parameters']['date']
            if num_date < 0:
                when = current + datetime.timedelta(days=num_date)
                events = Event.query.filter(Event.account_id == content['account_id'], Event.schedule_when == when)\
                    .order_by(Event.id)

                json_events = jsonify([{
                    "id": event.id,
                    "schedule_when": event.schedule_when,
                    "schedule_where": event.schedule_where,
                    "schedule_what": event.schedule_what,
                    "assign_time": event.assign_time,
                    "detail": event.detail,
                    "review": event.review
                } for event in events])

                if len(json_events) == 0:
                    result = {
                        "status": "Success",
                        "node_type": 0,
                        "message": ["그 날 알려준 이야기가 없네.. ㅠㅠ!", "혹시 다른 날이 아닐까?"],
                        "events": json_events
                    }
                result = {
                    "status": "Success",
                    "node_type": 2,
                    "message": ["일정들은 이렇게 돼!", "궁금한 날을 골라봐!"],
                    "events": json_events
                }

        result = reply
    db.session.commit()
    return jsonify(result)


# 추억회상 답장을 주는 로직
def reply_message_for_memory(content):
    # TODO : DB add
    result = {
        "status": "Failed",
    }
    max_index = len(content['response']['events'])
    if max_index <= content['response']['select_idx']:
        # 궁금한 일정이 없음
        result = {
            "status": "Success",
            "node_type": 0,
            "message": ["그래 또 궁금한 거 있으면 언제든지 물어봐!"],
            "events": []
        }
    else:
        select_idx = content['response']['select_idx']
        event = content['response']['events'][select_idx]
        message = []

        schedule = event['schedule_where'] + "에서 " + event['schedule_what']+"했었구나!"
        message.append(schedule)

        if event['detail'] != 'null':
            message.append("자세한 일정으로는 \""+event['detail']+"\"라고 말해줬어~")

        if event['review'] != 'null':
            message.append("그리고 그 일정을 다녀온 너는 \""+event['review']+"\"라고 나에게 이야기 해주었어!")

        result = {
            "status": "Success",
            "node_type": 2,
            "message": message,
            "events": content['response']['events']
        }

    return jsonify(result)


@bp.route('/messages/<int:res_account_id>')
def get_messages(res_account_id):
    # 사용자가 메세지 내역을 요청함
    chats = Chat.query.filter(Chat.account_id == res_account_id).order_by(Chat.id.desc()).limit(20).all()

    print(str(res_account_id), "왜그래.. ㅠㅠ")
    return jsonify([{
        "id": chat.id,
        "content": chat.content,
        "chat_type": chat.chat_type,
        "time": chat.time,
        "isBot": chat.isBot
    }for chat in chats])


@bp.route('/messages/<int:res_account_id>/<int:last_index>')
def get_more_messages(res_account_id, last_index):
    # 사용자가 메세지 내역을 요청함
    chats = Chat.query.filter(Chat.account_id == res_account_id, Chat.id < last_index)\
        .order_by(Chat.id.desc()).limit(50).all()
    return jsonify([{
        "id": chat.id,
        "content": chat.content,
        "chat_type": chat.chat_type,
        "time": chat.time,
        "isBot": chat.isBot
    }for chat in chats])


# end of message code

# start of event code
@bp.route('/events/<int:account_id>/<string:year>/<string:month>/<string:date>')
def get_events(account_id, year, month, date):
    date = year + "-" + month + "-" + date
    js = {
        "status": "Failed"
    }

    events = Event.query.filter(Event.account_id == account_id, Event.schedule_when == date).order_by(Event.id)
    return jsonify([{
        "id": event.id,
        "schedule_when": event.schedule_when,
        "schedule_where": event.schedule_where,
        "schedule_what": event.schedule_what,
        "assign_time": event.assign_time,
        "detail": event.detail,
        "review": event.review
    }for event in events])

# end of event code

