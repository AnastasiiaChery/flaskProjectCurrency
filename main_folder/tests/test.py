import pytest
from pymongo import settings

# from main_folder.auth import create_user
#
#
# @pytest.fixture(scope='session')
# def flask_db_setup():
#     settings.DATABASES['MONGODB_SETTINGS'] = {
#         'db': 'currency_db',
#         'host': 'localhost',
#         'port': 27017
#     }
#
# def test_create_user():
#     email = 'acher@mail.com'
#     password = '1234dfh'
#     name = 'Anna'
#     surname = 'Romanova'
#
#     create_user(email, password, name, surname)
    # print(user_res)

    # assert user_res == 200



# def test_passing():
#     assert (1, 2, 3) == (1, 2, 3)
#
# def test_failing():
#     assert (1, 2, 3) == (3, 2, 1)

from collections import namedtuple
Task = namedtuple('Task', ['summary', 'owner', 'done', 'id'])
Task.__new__.__defaults__ = (None, None, False, None)

def test_defaults():
    """Без использования параметров, следует ссылаться на значения по умолчанию."""
    t1 = Task()
    t2 = Task(None, None, False, None)
    assert t1 == t2

def test_member_access():
    """Проверка свойства .field (поля) namedtuple."""
    t = Task('buy milk', 'brian')
    assert t.summary == 'buy milk'
    assert t.owner == 'brian'
    assert (t.done, t.id) == (False, None)