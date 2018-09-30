from djbot.models.models import *

#   #   #   #   #   #
# DATABASE 컨트롤러 #
#   #   #   #   #   #


def insert_message_multiple(account_id, content, timestamp):
    for message in content['content']:
        insert_messages_single(account_id, message, content['node_type'], content['chat_type'], timestamp)


def insert_messages_single(account_id, message, node_tye, chat_type, timestamp):
    chat = Chat(account_id=account_id, content=message, node_type=node_tye, chat_type=chat_type, time=timestamp, isBot=1)
    db.session.add(chat)
    db.session.commit()


def insert_message_multiple_with_carousel(account_id, content, timestamp, carousel_list):
    for idx, message in enumerate(content['content']):
        if idx != (len(content['content'])-1):
            insert_messages_single(account_id, message, content['node_type'], content['chat_type'], timestamp)
        else:
            insert_messages_single_with_carousel(account_id, message, content['node_type'], content['chat_type'], timestamp, carousel_list)


def insert_messages_single_with_carousel(account_id, message, node_tye, chat_type, timestamp, carousel_list):
    chat = Chat(account_id=account_id, content=message, node_type=node_tye, chat_type=chat_type, time=timestamp,
                isBot=1, carousel_list=str(carousel_list))
    db.session.add(chat)
    db.session.commit()


# 토큰을 추가합니다.
def add_token(account_id, token):
    fcm_token = FcmToken(account_id=account_id, token=token)
    db.session.add(fcm_token)
    db.session.commit()


# 토큰을 삭제합니다.
def delete_token(account_id, token):
    tokens = FcmToken.query.filter(FcmToken.account_id == account_id, FcmToken.token == token).all()
    for token in tokens:
        db.session.delete(token)
    db.session.commit()
