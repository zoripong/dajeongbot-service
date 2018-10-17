import pytest
import json
from flask import url_for

from djbot.models.models import *


@pytest.mark.usefixtures('app')
class TestLogin:

    def test_add(self):
        success_account = CustomAccount(user_id='test', name='test', birthday='2000-05-09', account_type=0, bot_type=0,
                                        notify_time="08:00", ask_time="20:00", password='test')
        failed_account = CustomAccount(user_id='test2', name='test', birthday='2000-05-09', account_type=0, bot_type=0,
                                       notify_time="08:00", ask_time="20:00", password='test')

        db.session.add(success_account)
        db.session.commit()

        assert success_account in db.session
        assert failed_account not in db.session

    def login(self, user_id, password):
        return self.client.get('/user/0/test24/test', follow_redirects=True)

    # def test_login(self):
    #     rv = self.login('test', 'test')
    #     assert rv.data['status'] == 'NOT EXIST'
