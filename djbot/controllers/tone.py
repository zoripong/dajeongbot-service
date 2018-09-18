# coding=utf-8

bot_img = {
    "https://bit.ly/2oX627x": [
        "https://bit.ly/2oX627x",
        "https://bit.ly/2NycfEJ",
        "https://bit.ly/2oX627x",
        "https://bit.ly/2N2jgya"
    ],
    "hbd": [
        "https://bit.ly/2MFaz7T",
        "https://bit.ly/2NPEXRF",
        "https://bit.ly/2NWxekK",
        "https://bit.ly/2QBqJT4"
    ]
}


welcome_message = ["반가워요 무엇을 도와드릴까요?", "반가워요 무엇을 도와드릴까요?", "반가워요 무엇을 도와드릴까요?", "반가워요 무엇을 도와드릴까요?"]

danbee_message = {
    # 일정 등록
    # "FLOW1533045900000": {
    "SpeakNode_1533011459751": ["그래? 어떤 일이야?", "그래? 어떤 일이야?", "그래? 어떤 일이야?", "그래? 어떤 일이야?"],
    "SlotNode_1533084106826": ["무엇을 하나요?", "무엇을 하나요?", "무엇을 하나요?", "무엇을 하나요?"],
    "SlotNode_1533084109946": ["언제 하나요?", "언제 하나요?", "언제 하나요?", "언제 하나요?"],
    "SlotNode_1533084112968": ["어디서 하나요?", "어디서 하나요?", "어디서 하나요?", "어디서 하나요?"],
    "SpeakNode_1533045900031": ["알겠어! 내가 잘 기억해줄게!", "알겠어! 내가 잘 기억해줄게!", "알겠어! 내가 잘 기억해줄게!", "알겠어! 내가 잘 기억해줄게!"],
    "SlotNode_1533084740086": ["자세한 일정이 있어?", "자세한 일정이 있어?", "자세한 일정이 있어?", "자세한 일정이 있어?"],
    "SlotNode_1534819347535": ["그래? 알려주라!", "그래? 알려주라!", "그래? 알려주라!", "그래? 알려주라!"],
    "SpeakNode_1533084803517": ["그래! 좋은 시간 되었으면 좋겠다.", "그래! 좋은 시간 되었으면 좋겠다.",
                                "그래! 좋은 시간 되었으면 좋겠다.", "그래! 좋은 시간 되었으면 좋겠다."],
    # },
    # 추억 회상
    # "FLOW1533086390000": {
    "SlotNode_1533194947943": ["언제인데?", "언제인데?", "언제인데?", "언제인데?"],
    "SpeakNode_1533088123900": ["미래는 알 수 없는 법이지요..", "미래는 알 수 없는 법이지요..",
                                "미래는 알 수 없는 법이지요..", "미래는 알 수 없는 법이지요.."],
    "SpeakNode_1533088132355": ["잠시만요! 그때 무슨 일이 있었더라..", "잠시만요! 그때 무슨 일이 있었더라..",
                                "잠시만요! 그때 무슨 일이 있었더라..", "잠시만요! 그때 무슨 일이 있었더라.."],
    "SpeakNode_1533097409213": ["그래 또 궁금한거 있으면 언제든지 물어봐", "그래 또 궁금한거 있으면 언제든지 물어봐",
                                "그래 또 궁금한거 있으면 언제든지 물어봐", "그래 또 궁금한거 있으면 언제든지 물어봐"],
    # },
    # 채트플로우의 마지막으로 데이터가 넘어오지 않음
    # "last_node": {
    "SpeakNode_1536422714561": ["안녕 나는 다정군이야", "안녕 나는 다정냥이야", "안녕 나는 다정곰이야", "안녕 나는 다정몽이야"],
    # }
    "흥미롭군요 :D" : ["흥미롭군요 :D", "흥미롭군요 :D", "흥미롭군요 :D", "흥미롭군요 :D"]
}

memory_message = [  # memory_chat
    [  # bot type
        ["다정군 그래, 또 궁금한 거 있으면 물어봐!"],
        ["다정냥 그래, 또 궁금한 거 있으면 물어봐!2"],
        ["다정곰 그래, 또 궁금한 거 있으면 물어봐!2"],
        ["다정뭉 그래, 또 궁금한 거 있으면 물어봐!"]
    ],
    [
        ["다정군 잠시만요! 그때 무슨 일이 있었더라..", "그 날 알려준 이야기가 없네.. ㅠㅠ!", "혹시 다른 날이 아닐까?"],
        ["다정냥 잠시만요! 그때 무슨 일이 있었더라..", "그 날 알려준 이야기가 없네.. ㅠㅠ!", "혹시 다른 날이 아닐까?"],
        ["다정곰 잠시만요! 그때 무슨 일이 있었더라..", "그 날 알려준 이야기가 없네.. ㅠㅠ!", "혹시 다른 날이 아닐까?"],
        ["다정뭉 잠시만요! 그때 무슨 일이 있었더라..", "그 날 알려준 이야기가 없네.. ㅠㅠ!", "혹시 다른 날이 아닐까?"]
    ],
    [
        ["다정군 잠시만요! 그때 무슨 일이 있었더라..", "일정들은 이렇게 돼!", "궁금한 날을 골라봐!"],
        ["다정냥 잠시만요! 그때 무슨 일이 있었더라..", "일정들은 이렇게 돼!", "궁금한 날을 골라봐!"],
        ["다정곰 잠시만요! 그때 무슨 일이 있었더라..", "일정들은 이렇게 돼!", "궁금한 날을 골라봐!"],
        ["다정뭉 잠시만요! 그때 무슨 일이 있었더라..", "일정들은 이렇게 돼!", "궁금한 날을 골라봐!"]
    ]
]

schedule_message = [
    [
        ["또 들려줄 이야기가 있니?"],
        ["또 들려줄 이야기가 있니?"],
        ["또 들려줄 이야기가 있니?"],
        ["또 들려줄 이야기가 있니?"]
    ],
    [
        ["이제 오늘 이야기가 끝이네!", "고생 많았어~"],
        ["이제 오늘 이야기가 끝이네!", "고생 많았어~"],
        ["이제 오늘 이야기가 끝이네!", "고생 많았어~"],
        ["이제 오늘 이야기가 끝이네!", "고생 많았어~"]
    ],
    [
        ["오늘도 고생 많았어~"],
        ["오늘도 고생 많았어~"],
        ["오늘도 고생 많았어~"],
        ["오늘도 고생 많았어~"]
    ]
]

ask_review_message = [
    [
        ["오늘 하루 어땠니?"],
        ["오늘 하루 어땠니?"],
        ["오늘 하루 어땠니?"],
        ["오늘 하루 어땠니?"]
    ]
]

congratulate_birthday = [
    [
        ["생일 축하한다네"],
        ["생일 축하한다냥"],
        ["생일 축하해 :3"],
        ["생일 축하한다 뭉!"]
    ]
]


def convert_memory_message(event, bot_type):
    message = []
    if bot_type == 0:                                       # 다정군
        schedule = event['schedule_where'] + "에서 " + event['schedule_what'] + "했었구나!"
        message.append(schedule)

        if event['detail'] != 'null':
            message.append("자세한 일정으로는 \"" + event['detail'] + "\"라고 말해줬어~")

        if event['review'] != 'null':
            message.append("그리고 그 일정을 한 후 너는 \"" + event['review'] + "\"라고 나에게 이야기 해주었어!")

    elif bot_type == 1:                                       # 다정냥
        schedule = event['schedule_where'] + "에서 " + event['schedule_what'] + "했었구나!"
        message.append(schedule)

        if event['detail'] != 'null':
            message.append("자세한 일정으로는 \"" + event['detail'] + "\"라고 말해줬어~")

        if event['review'] != 'null':
            message.append("그리고 그 일정을 한 후 너는 \"" + event['review'] + "\"라고 나에게 이야기 해주었어!")

    elif bot_type == 2:                                       # 다정곰
        schedule = event['schedule_where'] + "에서 " + event['schedule_what'] + "했었구나!"
        message.append(schedule)

        if event['detail'] != 'null':
            message.append("자세한 일정으로는 \"" + event['detail'] + "\"라고 말해줬어~")

        if event['review'] != 'null':
            message.append("그리고 그 일정을 한 후 너는 \"" + event['review'] + "\"라고 나에게 이야기 해주었어!")

    elif bot_type == 3:                                       # 다정몽
        schedule = event['schedule_where'] + "에서 " + event['schedule_what'] + "했었구나!"
        message.append(schedule)

        if event['detail'] != 'null':
            message.append("자세한 일정으로는 \"" + event['detail'] + "\"라고 말해줬어~")

        if event['review'] != 'null':
            message.append("그리고 그 일정을 한 후 너는 \"" + event['review'] + "\"라고 나에게 이야기 해주었어!")
    else:
        schedule = event['schedule_where'] + "에서 " + event['schedule_what'] + "했었구나!"
        message.append(schedule)

        if event['detail'] != 'null':
            message.append("자세한 일정으로는 \"" + event['detail'] + "\"라고 말해줬어~")

        if event['review'] != 'null':
            message.append("그리고 그 일정을 한 후 너는 \"" + event['review'] + "\"라고 나에게 이야기 해주었어!")

    return message


def convert_schedule_message(event, bot_type):
    if bot_type == 0:
        return [event.schedule_where+"에서 "+event.schedule_what, "이건 오늘 어땠니"]
    elif bot_type == 1:
        return [event.schedule_where + "에서 " + event.schedule_what, "이건 오늘 어땠니"]
    elif bot_type == 2:
        return [event.schedule_where + "에서 " + event.schedule_what, "이건 오늘 어땠니"]
    elif bot_type == 4:
        return [event.schedule_where+"에서 "+event.schedule_what, "이건 오늘 어땠니"]
    return [event.schedule_where+"에서 "+event.schedule_what, "이건 오늘 어땠니"]


def convert_notification_message(event, bot_type):
    if bot_type == 0:
        return ["오늘은 일정이 있는 날이네!",
                event.schedule_where + "에서 " + event.schedule_what,
                "오늘도 화이팅!"]
    elif bot_type == 1:
        return ["오늘은 일정이 있는 날이네!",
                event.schedule_where + "에서 " + event.schedule_what,
                "오늘도 화이팅!"]
    elif bot_type == 2:
        return ["오늘은 일정이 있는 날이네!",
                event.schedule_where + "에서 " + event.schedule_what,
                "오늘도 화이팅!"]
    elif bot_type == 4:
        return ["오늘은 일정이 있는 날이네!",
                event.schedule_where + "에서 " + event.schedule_what,
                "오늘도 화이팅!"]

    return ["오늘은 일정이 있는 날이네!",
            event.schedule_where + "에서 " + event.schedule_what,
            "오늘도 화이팅!"]