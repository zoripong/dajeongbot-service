from flask import Blueprint, jsonify, request

from djbot.controllers.memory import reply_message_for_memory
from djbot.controllers.message import reply_message
from djbot.controllers.schedule import reply_message_for_reply_review, reply_message_for_select_review
from djbot.models.models import *

bp = Blueprint('message', __name__, url_prefix='/messages')


@bp.route('/', methods=['POST'])
def add_messages():
    # 사용자가 새로운 메세지를 보냄
    content = request.get_json(force=True)

    result = jsonify({"status": "Failed"})

    content_message = content['content'].split(':')

    if content['chat_type'] == 1 or content['chat_type'] == 4 or content['chat_type'] == 5:
        if len(content_message) == 2:
            content['content'] = content_message[1]

    chat = Chat(account_id=content['account_id'], content=content['content'], node_type=content['node_type'],
                chat_type=content['chat_type'], time=content['time'], isBot=content['isBot'])
    db.session.add(chat)
    db.session.commit()

    print("채트 타입입니다. : ", content['chat_type'])

    # 챗봇이랑 대화 chat_type 으로 분류
    # try:
    if content['chat_type'] == 0 or content['chat_type'] == 1:
        result = reply_message(content)
    elif content['chat_type'] == 2:
        result = reply_message_for_memory(content)
    elif content['chat_type'] == 4:
        result = reply_message_for_select_review(content, content_message[0])
    elif content['chat_type'] == 5:
        result = reply_message_for_reply_review(content, content_message[0])
    # except TypeError as err:
    #     print("TYPE error: {0}".format(err))
    #     result = reply_message(content)

    return result


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
        "carousel_list": chat.carousel_list,
        "slot_list": chat.slot_list
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
        "carousel_list": chat.carousel_list,
        "slot_list": chat.slot_list
    }for chat in chats])
