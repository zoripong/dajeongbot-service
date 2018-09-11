import datetime
import time

from flask import jsonify

from djbot.controllers.data import insert_message_multiple
from djbot.models.models import *

#   #   #   #   #   #
#  추억 회상 컨트롤러 #
#   #   #   #   #   #


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
            # TODO db 저장
            result_json = {
                "status": "Success",
                "result": {
                    "id": content['account_id'],
                    "node_type": 0,
                    "chat_type": content['chat_type'],
                    "time": str(int(time.time() * 1000)),
                    "img_url": [],
                    "content": ["잠시만요! 그때 무슨 일이 있었더라..", "그 날 알려준 이야기가 없네.. ㅠㅠ!", "혹시 다른 날이 아닐까?"],
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
                    "content": ["잠시만요! 그때 무슨 일이 있었더라..", "일정들은 이렇게 돼!", "궁금한 날을 골라봐!"],
                    "events": json_events
                }
            }
        print(type(result_json))
        insert_message_multiple(content['account_id'], result_json['result'], result_json['result']['time'])

    return result_json

