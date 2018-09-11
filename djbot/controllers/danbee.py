import requests
import json
import config

# request module
# http://dgkim5360.tistory.com/entry/python-requests

#   #   #   #   #   #
#   챗봇 엔진 연결   #
#   #   #   #   #   #

URL = 'https://danbee.ai/chatflow/engine.do'
WELCOME_URL = 'https://danbee.ai/chatflow/welcome.do'

headers = {'Content-Type': 'application/json; charset=utf-8'}


def welcome():
    data = {
        "chatbot_id": config.CHATBOT_CONFIG['chatbot_id'],
        "parameters": {}
    }
    res = requests.post(WELCOME_URL, headers=headers, data=json.dumps(data))
    return res.json()


def message_with_response(content, response):
    data = {
        "chatbot_id": config.CHATBOT_CONFIG['chatbot_id'],
        "input_sentence": content,
        "user_id": "",
        "session_id": "",
        "ins_id": "",
        "intent_id": "",
        "node_id": "",
        "param_id": "",
        "chatflow_id": "",
        "parameters": {}
    }
    # print("response\n", response)
    if "version" in response:
        data = {
            "chatbot_id": config.CHATBOT_CONFIG['chatbot_id'],
            "input_sentence": content,
            "user_id": response['user_id'],
            "session_id": response['user_id'],
            "ins_id": response['ins_id'],
            "intent_id": response['intent_id'],
            "node_id": response['node_id'],
            "param_id": response['param_id'],
            "chatflow_id": response['chatflow_id'],
            "parameters": {}
        }

    # print("send\n", data)
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    return res.json()


def message(content):
    data = {
        "chatbot_id": config.CHATBOT_CONFIG['chatbot_id'],
        "input_sentence": content,
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
    return res.json()
