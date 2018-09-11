import calendar
import datetime
import time

from flask import jsonify

from djbot.controllers import danbee
from djbot.controllers.memory import get_memory
from djbot.controllers.schedule import register_event
from djbot.models.models import *
from config import NODE_TYPE

#   #   #   #   #   #
#  메세지 컨트롤러  #
#   #   #   #   #   #

def add_message_for_new_user(account_id):
    ts = calendar.timegm(time.gmtime())
    content = '반가워요 무엇을 도와드릴까요?'
    chat = Chat(account_id=account_id, content=content, node_type=0, chat_type=0, time=str(ts), isBot=1)
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

        if bot_message == "잠시만요! 그때 무슨 일이 있었더라..":
            result_json = get_memory(reply, content, current)
        else:
            if bot_message == "그래! 좋은 시간 되었으면 좋겠다.":
                result_json = reply
                register_event(reply, result, content['account_id'])
            else:
                result_json = reply

            # node type
            # speak=0 slot=1 carousel=2
            chat = Chat(account_id=content['account_id'], content=bot_message, node_type=NODE_TYPE[node_type],
                        chat_type=content['chat_type'], time=str(int(time.time() * 1000)), isBot=1)
            db.session.add(chat)

    db.session.commit()
    print(result_json)
    return jsonify(result_json)