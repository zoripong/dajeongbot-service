import calendar
import datetime
import time

from flask import Blueprint, jsonify, request

from djbot.controllers import danbee
from djbot.controllers.schedule import register_event
from djbot.models.models import *
from config import NODE_TYPE

bp = Blueprint('message', __name__, url_prefix='/messages')


@bp.route('/', methods=['POST'])
def add_messages():
    # 사용자가 새로운 메세지를 보냄
    content = request.get_json(force=True)

    result = jsonify({"status": "Failed"})

    contents = content['content'].split(':')
    if content['chat_type'] == 4 or content['chat_type'] == 5:
        if len(contents) == 2:
            content['content'] = contents[1]

    chat = Chat(account_id=content['account_id'], content=content['content'], node_type=content['node_type'],
                chat_type=content['chat_type'], time=content['time'], isBot=content['isBot'])
    db.session.add(chat)
    db.session.commit()

    print("채트 타입입니다. : ", content['chat_type'])
    # 챗봇이랑 대화 chat_type 으로 분류
    if content['chat_type'] == 0 or content['chat_type'] == 1:
        result = reply_message(content)
    elif content['chat_type'] == 2:
        result = reply_message_for_memory(content)
    elif content['chat_type'] == 4:
        result = reply_message_for_select_review(content, contents['response']['select_idx'])
    elif content['chat_type'] == 5:
        result = reply_message_for_reply_review(content, contents['response']['select_idx'])

    return result


def add_message_for_new_user(account_id):
    ts = calendar.timegm(time.gmtime())
    # TODO : 캐릭터 컨셉으로 변환
    content = '반가워요 무엇을 도와드릴까요?'

    chat = Chat(account_id=account_id, content=content, node_tyoe=0, chat_type=0, time=str(ts), isBot=1)
    db.session.add(chat)
    db.session.commit()


# 챗봇이 답장을 주는 부분
def reply_message(content):
    current = datetime.datetime.now()
    # 챗봇
    reply = danbee.message_with_response(content['content'], content['response'])
    reply_result = reply['responseSet']['result']['result']

    for result in reply_result:
        img_url = result['imgRoute']
        if img_url is not None and img_url != "":
            chat = Chat(account_id=content['account_id'], content=img_url, node_type=NODE_TYPE['img'],
                        chat_type=content['chat_type'],
                        time=str(int(time.time() * 1000)), isBot=1)
            db.session.add(chat)

        bot_message = result['message']
        node_type = result['nodeType']

        if reply['responseSet']['result']['ins_id'] == "" \
                and reply['responseSet']['result']['ref_intent_id'] == "":
            result_json = {
                "status": "Intent is not Found",
            }

        if bot_message == "그래! 좋은 시간 되었으면 좋겠다.":
            register_event(reply, result, content['account_id'])
        elif bot_message == "잠시만요! 그때 무슨 일이 있었더라..":
            node_type = 'carousel'
            num_date = int(reply['responseSet']['result']['parameters']['date'])
            if num_date < 0:
                when = current + datetime.timedelta(days=num_date)
                events = Event.query.filter(Event.account_id == content['account_id'], Event.schedule_when == when) \
                    .order_by(Event.id).all()

                json_events = [{
                    "id": event.id,
                    "schedule_when": event.schedule_when,
                    "schedule_where": event.schedule_where,
                    "schedule_what": event.schedule_what,
                    "assign_time": event.assign_time,
                    "detail": event.detail,
                    "review": event.review
                } for event in events]

                json_events = []
                for event in events:
                    json_events.append({
                        "id": event.id,
                        "event_detail": event.schedule_where+"에서 "+event.schedule_what,
                        "event_image": "",
                        "detail": event.detail,
                        "review": event.review
                    })

                if len(events) == 0:
                    # TODO db 저장
                    result_json = {
                        "status": "Success",
                        "result": {
                            "id": content['account_id'],
                            "node_type": 0,
                            "chat_type": content['chat_type'],
                            "time": str(int(time.time() * 1000)),
                            "img_url": [],
                            "content": ["그 날 알려준 이야기가 없네.. ㅠㅠ!", "혹시 다른 날이 아닐까?"],
                            "events": json_events
                        }

                    }
                else:
                    result_json = {
                        "status": "Success",
                        "result": {
                            "id": content['account_id'],
                            "node_type": 2,
                            "chat_type": 1,
                            "time": str(int(time.time() * 1000)),
                            "img_url": [],
                            "content": ["일정들은 이렇게 돼!", "궁금한 날을 골라봐!"],
                            "events": json_events
                        }
                    }
                print(type(result_json))
        else:
            result_json = reply
        # node type
        # speak=0 slot=1 carousel=2
        chat = Chat(account_id=content['account_id'], content=bot_message, node_type=NODE_TYPE[node_type],
                    chat_type=content['chat_type'], time=str(int(time.time() * 1000)), isBot=1)
        db.session.add(chat)

    db.session.commit()
    print("리턴 결과")
    print(result_json)
    return jsonify(result_json)


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
            "result": {
                "id": content['account_id'],
                "node_type": 0,
                "chat_type": content['chat_type'],
                "time": str(int(time.time() * 1000)),
                "img_url":[],
                "content": ["그래, 또 궁금한 거 있으면 물어봐!"],
                "events": []
            }
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
            "result":{
                "id": content['account_id'],
                "node_type": 2,
                "chat_type": content['chat_type'],
                "time": str(int(time.time() * 1000)),
                "img_url":[],
                "content": message,
                "events": content['response']['events']
            }
        }

    return jsonify(result)


# 일정등록 답장을 주는 로직
# 후기를 남길 이벤트를 선택함 -> 질문을 해줌
def reply_message_for_select_review(content, select_idx):
    now = str(int(time.time() * 1000))
    result = {}
    if select_idx == -1:
        # 이제 그만 등록하겠습니당
        messages = ["오늘도 고생 많았어~"]
        result = {
            "status": "Success",
            "result": {
                "id": content['account_id'],
                "node_type": 0,
                "chat_type": 0,
                "time": now,
                "img_url": [],
                "content": messages,
                "events": []
            }
        }
    else:
        # 이벤트 가져오기
        event = Event.query.filter(Event.event_id == select_idx)
        event_json = [{
            "id": event['id'],
            "account_id": event['account_id'],
            "schedule_when": event['schedule_when'],
            "schedule_where": event['schedule_where'],
            "schedule_what": event['schedule_what'],
            "assign_time": event['assign_time'],
            "detail": event['detail'],
            "review": event['review'],
            "notification_send": event['notification_send'],
            "question_send": event['question_send']
        }]

        messages = [event.schedule_where+"에서 "+event.schedule_what, "이건 오늘 어땠니"]
        # 이벤트 내용 보내주기
        result = {
            "status": "Success",
            "result": {
                "id": content['account_id'],
                "node_type": 0,
                "chat_type": content['chat_type'],  # 4
                "time": now,
                "img_url": [],
                "content": messages,
                "events": event_json
            }
        }

    insert_message_multiple(content['account_id'], content=result['result'], timestamp=now)

    return jsonify(result)


# 일정등록 답장을 주는 로직
# 후기를 남김 -> 더 물어볼지 이벤트 리스트를 넘김
def reply_message_for_reply_review(content, select_idx):
    now = str(int(time.time() * 1000))

    # 이벤트 후기 db 업데이트
    select_event = Event.query.filter(Event.id == select_idx)
    select_event.review = content['content']
    db.session.commit()

    # 이벤트 리스트를 넘김
    events = Event.query \
        .filter(Event.review.is_(None), Event.schedule_when == today, Event.account_id == content['account_id']) \
        .order_by(Event.id).all()

    if len(events) > 0:
        event_json = []
        for event in events:
            event_json.append({
                "id": event['id'],
                "account_id": event['account_id'],
                "schedule_when": event['schedule_when'],
                "schedule_where": event['schedule_where'],
                "schedule_what": event['schedule_what'],
                "assign_time": event['assign_time'],
                "detail": event['detail'],
                "review": event['review'],
                "notification_send": event['notification_send'],
                "question_send": event['question_send']
            })

        content = ["또 들려줄 이야기가 있니?"]
        result = {
            "status": "Success",
            "result": {
                "id": content['account_id'],
                "node_type": 2,
                "chat_type": content['chat_type'], # 5
                "time": now,
                "img_url": [],
                "content": content,
                "events": event_json
            }
        }
    else:
        messages = ["이제 오늘 이야기가 끝이네!", "고생 많았어~"]
        result = {
            "status": "Success",
            "result": {
                "id": content['account_id'],
                "node_type": 0,
                "chat_type": 0,
                "time": now,
                "img_url": [],
                "content": messages,
                "events": []
            }
        }

    insert_message_multiple(content['account_id'], content=result['result'], timestamp=now)
    return jsonify(result)


def insert_message_multiple(account_id, content, timestamp):
    for message in content['content']:
        insert_messages_single(account_id, message, content['node_type'], content['chat_type'], timestamp)


def insert_messages_single(account_id, message, node_tye, chat_type, timestamp):
    chat = Chat(account_id=account_id, content=message, node_tye=node_tye, chat_type=chat_type, time=timestamp, isBot=1)
    db.session.add(chat)
    db.session.commit()


@bp.route('/<int:res_account_id>')
def get_messages(res_account_id):
    # 사용자가 메세지 내역을 요청함
    chats = Chat.query.filter(Chat.account_id == res_account_id).order_by(Chat.id.desc()).limit(20).all()
    return jsonify([{
        "id": chat.id,
        "content": chat.content,
        "node_type": chat.node_type,                         # 모든 이전의 대화를 speak 로 바꿈..
        "chat_type": chat.chat_type,
        "time": chat.time,
        "isBot": chat.isBot,
        "carousel_list": chat.carousel_list
    }for chat in chats])


@bp.route('/<int:res_account_id>/<int:last_index>')
def get_more_messages(res_account_id, last_index):
    # 사용자가 메세지 내역을 요청함
    chats = Chat.query.filter(Chat.account_id == res_account_id, Chat.id < last_index)\
        .order_by(Chat.id.desc()).limit(50).all()
    return jsonify([{
        "id": chat.id,
        "content": chat.content,
        "node_type": chat.node_type,
        "chat_type": chat.chat_type,
        "time": chat.time,
        "isBot": chat.isBot,
        "carousel_list": chat.carousel_list
    }for chat in chats])
