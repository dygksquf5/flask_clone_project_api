



##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######
##### 일단보류 !!!! #######

import pytest
from app.main import create_app

from flask import g



@pytest.fixture
def api():
    app = create_app(config_name='test')
    app.config['TEST'] = True
    api = app.test_client()

    return api


@pytest.fixture(scope='function')
def session(db):
    session = db['session']()
    g.db = session

    yield session
    session.rollback()
    session.close()


# def setup_function():
#     pass
#
# def teardown_function():
#     pass


def test_ping(api):
    resp = api.get('/user/ping')
    assert b'pong' in resp.data
