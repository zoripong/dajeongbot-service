import datetime
import time
from random import randint

from flask import jsonify

from djbot.controllers.data import insert_message_multiple, insert_message_multiple_with_carousel
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
    # max_index = len(content['response']['events'])
    # print(max_index)
    # if "version" in response:
    if content['response']['select_idx'] == -1:
        # 궁금한 일정이 없음
        messages = memory_message[0][content['bot_type']][randint(0, 3)]
        result_json = {
            "status": "Success",
            "result": {
                "id": content['account_id'],
                "node_type": 0,
                "chat_type": 0,
                "time": str(int(time.time() * 1000)),
                "img_url": [],
                "content": messages,
                "events": []
            }
        }
        insert_message_multiple(
            content['account_id'],
            result_json['result'],
            result_json['result']['time']
        )

    else:
        select_idx = content['response']['select_idx']

        # FIXME ? DB쿼리말구..?
        event = Event.query.filter(Event.id == select_idx).all()

        messages = convert_memory_message(
            event[0], content['bot_type'], randint(0, 3)
        )
        print(content['response']['events'])
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

        insert_message_multiple_with_carousel(
            content['account_id'],
            result_json['result'],
            result_json['result']['time'],
            content['response']['events']
        )
    return jsonify(result_json)


def get_memory(reply, content, current):
    result_json = {"status": "Failed"}
    num_date = int(reply['responseSet']['result']['parameters']['date'])
    if num_date < 0:
        when = current + datetime.timedelta(days=num_date)
        when = when.strftime("%Y-%m-%d")
        events = Event.query.filter(
            Event.account_id == content['account_id'],
            Event.schedule_when == when
        ).order_by(Event.id).all()
        json_events = []
        event_detail = event.schedule_where + "에서 " + event.schedule_what
        for event in events:
            json_events.append({
                "id": event.id,
                "event_detail": event_detail,
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
                    "chat_type": 0,
                    "time": str(int(time.time() * 1000)),
                    "img_url": [],
                    "content":
                        memory_message[1][content['bot_type']][randint(0, 3)],
                    "events": json_events
                }

            }
            insert_message_multiple(
                content['account_id'],
                result_json['result'],
                result_json['result']['time']
            )
        else:
            result_json = {
                "status": "Success",
                "result": {
                    "id": content['account_id'],
                    "node_type": 2,
                    "chat_type": 2,
                    "time": str(int(time.time() * 1000)),
                    "img_url": [],
                    "content":
                        memory_message[2][content['bot_type']][randint(0, 3)],
                    "events": json_events
                }
            }
            insert_message_multiple_with_carousel(
                content['account_id'],
                result_json['result'],
                result_json['result']['time'],
                json_events
            )
    return result_json

