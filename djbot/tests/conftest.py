import os
import tempfile

import pytest

from app import create_app


@pytest.fixture
def client():

    app = create_app()

    app.debug = True
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    app_context = app.app_context()
    app_context.push()

    yield app.test_client()
    app_context.pop()

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

