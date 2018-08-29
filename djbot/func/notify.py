from pyfcm import FCMNotification
import config

push_service = FCMNotification(api_key=config.FCM_API)

