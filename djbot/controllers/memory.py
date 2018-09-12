import datetime
import time

from flask import jsonify

from djbot.controllers.data import insert_message_multiple
from djbot.controllers.tone import convert_memory_message, memory_message
from djbot.models.models import *

#   #   #   #   #   #   #
#   추억 회상 컨트롤러  #
#   #   #   #   #   #   #


# 추억회상 답장을 주는 로직
def reply_message_for_memory(content):
    result_json = {
        "status": "Failed",
    }
    messages = []
    max_index = len(content['response']['events'])
    if max_index <= content['response']['select_idx']:
        # 궁금한 일정이 없음
        messages = memory_message[0][content['bot_type']]
        result_json = {
            "status": "Success",
            "result": {
                "id": content['account_id'],
                "node_type": 0,
                "chat_type": content['chat_type'],
                "time": str(int(time.time() * 1000)),
                "img_url": [],
                "content": messages,
                "events": []
            }
        }
    else:
        select_idx = content['response']['select_idx']
        event = content['response']['events'][select_idx]
        messages = convert_memory_message(event, type)

        result_json = {
            "status": "Success",
            "result":{
                "id": content['account_id'],
                "node_type": 2,
                "chat_type": content['chat_type'],
                "time": str(int(time.time() * 1000)),
                "img_url": [],
                "content": messages,
                "events": content['response']['events']
            }
        }

    insert_message_multiple(content['account_id'], result_json['result'], result_json['result']['time'])

    return jsonify(result_json)


def get_memory(reply, content, current):
    result_json = {"status": "Failed"}
    node_type = 'carousel'
    num_date = int(reply['responseSet']['result']['parameters']['date'])
    if num_date < 0:
        when = current + datetime.timedelta(days=num_date)
        events = Event.query.filter(Event.account_id == content['account_id'], Event.schedule_when == when) \
            .order_by(Event.id).all()
        json_events = []
        for event in events:
            json_events.append({
                "id": event.id,
                "event_detail": event.schedule_where + "에서 " + event.schedule_what,
                "event_image": "",
                "detail": event.detail,
                "review": event.review
            })
        if len(json_events) == 0:
            result_json = {
                "status": "Success",
                "result": {
                    "id": content['account_id'],
                    "node_type": 0,
                    "chat_type": content['chat_type'],
                    "time": str(int(time.time() * 1000)),
                    "img_url": [],
                    "content": memory_message[1][content['bot_type']],
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
                    "content": memory_message[2][content['bot_type']],
                    "events": json_events
                }
            }
        print(type(result_json))
        insert_message_multiple(content['account_id'], result_json['result'], result_json['result']['time'])

    return result_json

