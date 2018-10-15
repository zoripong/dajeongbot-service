import os
import tempfile
import pytest
import worker


@pytest.fixture
def client():
    db_fd, worker.app.config['DATABASE'] = tempfile.mkstemp()
    worker.app.config['TESTING'] = True
    client = worker.app.test_client()

    with worker.app.app_context():
        worker.init_db()

    yield client

    os.close(db_fd)
    os.unlink(worker.app.config['DATABASE'])