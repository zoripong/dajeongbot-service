from flask import Blueprint, request, jsonify

from djbot import db
from djbot.models.models import *
import djbot.models.models as model
import json


bp = Blueprint('api', __name__, url_prefix='/apis')

# test code


@bp.route("/")
def hello_world():
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


# end of test code

# start of auth code
@bp.route('/users/<int:account_type>/<string:user_id>/<string:password>')
def login(account_type, user_id, password):

    j1 = [{
        "status": "Failed",
    }]
    if account_type == 0:
        account = CustomAccount.query.filter(CustomAccount.user_id == user_id, CustomAccount.password == password,
                                             CustomAccount.account_type == account_type).all()
        if len(account) == 1:
            j1 = [{
                "status": "OK",
                "user_info": {
                    "id": account[0].id,
                    "bot_type": account[0].bot_type,
                    "chat_session": "preparing"
                }
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
    content = request.get_json(force=True)

    # 존재하는 아이디인지 체크
    result = {
        "status": "Failed"
        # "id": content["user_id"]
    }
    print(type(content['account_type']))
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
        result = {
            "status": "Success"
        }

    return json.dumps(result)


# end of auth code

# start of message code
@bp.route('/messages', methods=['POST'])
def add_messages():
    # 사용자가 새로운 메세지를 보냄
    content = request.get_json(force=True)

    result = {"status": "Failed"}

    chat = Chat(account_id=content['account_id'], content=content['content'], chat_type=content['chat_type'],
                time=content['time'], isBot=content['isBot'])
    db.session.add(chat)
    db.session.commit()

    reply_message(content)

    result = {"status": "Success"}

    return json.dumps(result)


# 챗봇이 답장을 주는 부분
def reply_message(content):

    # content = jsonify(data)

    chat = Chat(account_id=content['account_id'], content=content['content']+"reply", chat_type=content['chat_type'],
                time=content['time'], isBot=1)
    db.session.add(chat)
    db.session.commit()
    print(content['account_id'])


@bp.route('/messages/<int:account_id>')
def get_messages(account_id):
    # 사용자가 메세지 내역을 요청함
    chats = Chat.query.filter(account_id == account_id).order_by(Chat.id.desc()).limit(20)
    return jsonify([{
        "id": chat.id,
        "content": chat.content,
        "chat_type": chat.chat_type,
        "time": chat.time,
        "isBot": chat.isBot
    }for chat in chats])


@bp.route('/messages/<int:account_id>/<int:last_index>')
def get_more_messages(account_id, last_index):
    # 사용자가 메세지 내역을 요청함
    chats = Chat.query.filter(account_id == account_id, Chat.id < last_index).order_by(Chat.id.desc()).limit(50)
    return jsonify([{
        "id": chat.id,
        "content": chat.content,
        "chat_type": chat.chat_type,
        "time": chat.time,
        "isBot": chat.isBot
    }for chat in chats])


# end of message code

# start of event code


# end of event code

