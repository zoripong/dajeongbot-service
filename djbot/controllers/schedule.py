import datetime
import time

from flask import jsonify

from djbot.controllers.data import insert_message_multiple
from djbot.models.models import *

#   #   #   #   #   #
#  일정 등록 컨트롤러 #
#   #   #   #   #   #


# 일정등록 답장을 주는 로직
def register_event(reply, content, account_id):
    current = datetime.datetime.now()
    param = reply['responseSet']['result']['parameters']
    message_result = reply['responseSet']['result']['result']
    when = current + datetime.timedelta(days=int(param['when']))
    when = when.strftime('%Y-%m-%d')

    event = Event(account_id=account_id, schedule_when=when, schedule_where=param['where'],
                  schedule_what=param['what'], assign_time=message_result[0]['timestamp'],
                  detail=param['detail_content'])
    db.session.add(event)


# 일정등록 답장을 주는 로직
# 후기를 남김 -> 더 물어볼지 이벤트 리스트를 넘김
def reply_message_for_reply_review(content, select_idx):
    now = str(int(time.time() * 1000))
    today = datetime.datetime.now().strftime("%Y-%m-%d")

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
