import requests
import json
import config

# request module
# http://dgkim5360.tistory.com/entry/python-requests

URL = 'https://danbee.ai/chatflow/engine.do'
WELCOME_URL = 'https://danbee.ai/chatflow/welcome.do'

headers = {'Content-Type': 'application/json; charset=utf-8'}


# test method
def hello():
    data = {
        "chatbot_id": config.CHATBOT_CONFIG['chatbot_id'],
        "input_sentence": "나 할 일 생겼다.",
        "user_id": "",
        "session_id": "",
        "ins_id": "",
        "intent_id": "",
        "node_id": "",
        "param_id": "",
        "chatflow_id": "",
        "parameters": {}
    }

    res = requests.post(URL, headers=headers, data=json.dumps(data))
    print(res.json())
# end of test method


def welcome():
    data = {
        "chatbot_id": config.CHATBOT_CONFIG['chatbot_id'],
        "parameters": {}
    }
    res = requests.post(WELCOME_URL, headers=headers, data=json.dumps(data))
    return res.json()

