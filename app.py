from flask import Flask
from djbot.models import models
from djbot.models.models import Account


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://djbot:djbotAdmin2018*@119.205.221.104/DajeongBot"
    models.db.init_app(app)

    @app.route('/')
    def hello_word():
        user = Account(user_id="test", name="test", birthday="2000.05.09.", account_type=1, bot_type=1)
        models.db.session.add(user)
        models.db.session.commit()
        return 'hello'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

