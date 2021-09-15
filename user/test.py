from http import client
from urllib import response

import pytest
from aiohttp.web_routedef import route


class TestAutentification:
    def test_one(self):
        url = route('/profile', methods=['POST'])

        data = {
            'email': '123@mail.com',
            'password': '1234abc',
            'name':'inna',
            'surname': 'ivanova'

        }

        response = client.post(url, json=data)
        assert response.status_code == 200


    # def test_two(self):
    #     assert 0