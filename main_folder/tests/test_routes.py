import unittest
import jwt

from datetime import datetime, timedelta
from main_folder import app
from main_folder.auth import JWT_SECRET, JWT_ALGORITHM

toc = jwt.encode({'email': 'irin212a123@gmail.com', 'exp': datetime.utcnow() + timedelta(minutes=130)}, JWT_SECRET,
                 JWT_ALGORITHM)


class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_page(self):
        rv = self.app.get('/', headers={'x-access-tokens': toc})
        assert rv.status == '200 OK'

    def test_select_currency_by_data(self):
        rv = self.app.post('/by_date', data={'date': 2021913}, headers={'x-access-tokens': toc})
        assert rv.status == '200 OK'

    def test_change_base_currency(self):
        rv = self.app.post('/select', data={'date': 2021913, 'curr_id': 'eur'}, headers={'x-access-tokens': toc})
        assert rv.status == '200 OK'

    def test_currency_characteristic(self):
        rv = self.app.post('/characteristic',
                           data={'st_date': 2021913, 'ls_date': 2021916, 'code': 'usd', 'action': 'max'}, headers={'x-access-tokens': toc})
        rv1 = self.app.post('/characteristic',
                            data={'st_date': 2021913, 'ls_date': 20211016, 'code': 'cad', 'action': 'min'}, headers={'x-access-tokens': toc})
        rv2 = self.app.post('/characteristic',
                            data={'st_date': 2021913, 'ls_date': 20211016, 'code': 'eur', 'action': 'mean'}, headers={'x-access-tokens': toc})
        rv3 = self.app.post('/characteristic',
                            data={'st_date': 2021913, 'ls_date': 2021916, 'code': 'afv', 'action': 'max'},  headers={'x-access-tokens': toc})
        rv4 = self.app.post('/characteristic',
                            data={'st_date': 2021913, 'ls_date': 2021916, 'code': 'eur', 'action': 'mx'},  headers={'x-access-tokens': toc})
        assert rv.status == '200 OK'
        assert rv.data.decode() == '26.692\n'
        assert rv1.data.decode() == '20.8773\n'
        assert rv2.data.decode() == '30.84286875\n'
        assert rv3.status == '500 INTERNAL SERVER ERROR'
        assert rv4.status == '500 INTERNAL SERVER ERROR'

    def test_currency_converter(self):
        rv = self.app.post('/currency-converter', data={'from': 'EUR', 'to': 'USD', 'sum': '100', 'date': 2021914},
                           headers={'x-access-tokens': toc})
        rv1 = self.app.post('/currency-converter', data={'from': 'xpd', 'to': 'USD', 'sum': '100', 'date': 2021914},
                            headers={'x-access-tokens': toc})

        rv3 = self.app.post('/currency-converter', data={'from': 'xpd', 'to': 'UD', 'sum': '30'},
                            headers={'x-access-tokens': toc})
        assert rv.status == '200 OK'
        assert rv.data.decode() == '118.12007718818751\n'
        assert rv1.data.decode() == '197895.00754612146\n'
        assert rv3.status == '500 INTERNAL SERVER ERROR'
