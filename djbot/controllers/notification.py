from pyfcm import FCMNotification

import config

push_service = FCMNotification(api_key=config.FCM_API)


def notify(token, title, message):
    return push_service.notify_single_device(registration_id=token, message_title=title, message_body=message)

