import unittest

from requests.auth import _basic_auth_str

from main_folder import app


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_login_user(self):
        rv = self.app.post('/login', headers={'Authorization': _basic_auth_str('irin212a123@gmail.com', '1234anna')})
        rv2 = self.app.post('/login', headers={'Authorization': _basic_auth_str('idsfvs3@gmail.com', '12sdvnna')})
        assert rv.status == '200 OK'
        assert ('token' in rv.data.decode()) == True
        assert rv2.status == '500 INTERNAL SERVER ERROR'

    # def test_logout(self):
    #     rv = self.app.post('/login', headers={token})
    #     assert rv.status == '200 OK'

