from pyfcm import FCMNotification
import config

push_service = FCMNotification(api_key=config.FCM_API)


def notify():
    registration_id = "ecEigPKJXf0:APA91bFWZkgS-tNpXnQ9Ea0TEASr0EXTiyOGhYoMbtgn75TrR2Y3TF2KbDx1SbkdovEdBuibp262SiVFCjwIPJAWQNg9kKlOx4MaurbpIxVVYaSpa5vJylZKidbieoyMEU53R5brmLQz"
    message_title = "Uber update"
    message_body = "Hi john, your customized news for today is ready"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    return result