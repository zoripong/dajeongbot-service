import os
import tempfile

import pytest

from app import create_app

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    app.debug = True
    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path
    app.PRESERVE_CONTEXT_ON_EXCEPTION = False


    # with app.app_context():
    #     init_db()
    #     get_db().executescript(_data_sql)

    # app.app_context().push()

    yield app

    app.app_context().pop()

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()