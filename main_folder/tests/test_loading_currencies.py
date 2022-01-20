import json

import pandas as pd
from main_folder.loading_currencies import get_data_from_app, create_curr


def test_get_data_from_app(monkeypatch):
    execute_counter = 0

    def mock_get_data_from_app_response(*args, **kwargs):
        get_data = pd.read_json("template.txt")
        return get_data

    monkeypatch.setattr(json, 'loads', mock_get_data_from_app_response)

    def mock_create_curr(*args, **kwargs):
        nonlocal execute_counter
        execute_counter += 1


    monkeypatch.setattr('main_folder.loading_currencies.create_curr', mock_create_curr)

    get_data_from_app()

    assert execute_counter == 3
