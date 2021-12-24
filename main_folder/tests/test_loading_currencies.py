import json
from unittest.mock import patch, Mock, mock_open

import requests

from github.NamedUser import NamedUser


from main_folder.loading_currencies import get_data_from_app, create_curr
from unittest.mock import Mock


def test_get_data_from_app(monkeypatch):
    execute_counter=0

    def mock_get_data_from_app_res(*args, **kwargs):
        response=open('template.json', 'r')
        return response


    def mock_create_curr(*args, **kwargs):
        nonlocal execute_counter
        execute_counter+=1


    monkeypatch.setattr(requests, "get", mock_get_data_from_app_res)
    # monkeypatch.setattr(json, "loads", mock_get_data_from_app_response)
    monkeypatch.setattr('main_folder.loading_currencies.create_curr', mock_create_curr)

    get_data_from_app()

    assert execute_counter==1





