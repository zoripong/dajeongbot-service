import requests
import json

# request module
# http://dgkim5360.tistory.com/entry/python-requests

URL = 'https://danbee.ai/chatflow/engine.do'

# test method


def hello():
    data = {
        "chatbot_id": "9c94e975-49c8-4a08-bdfe-b19085ecf42f",
        "input_sentence": "나 할 일 생겼다.",
        "user_id": "",
        "session_id": "",
        "ins_id": "",
        "intent_id": "",
        "node_id": "",
        "param_id": "",
        "chatflow_id": "",
        "parameters":{}
    }

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    print(res.json())
# end of test method
