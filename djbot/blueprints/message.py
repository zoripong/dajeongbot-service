import calendar
import datetime
import time

from flask import Blueprint, jsonify, request

from djbot.blueprints import danbee
from djbot.models.models import *

bp = Blueprint('message', __name__, url_prefix='/messages')


@bp.route('/', methods=['POST'])
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


@bp.route('/<int:res_account_id>')
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


@bp.route('/<int:res_account_id>/<int:last_index>')
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
