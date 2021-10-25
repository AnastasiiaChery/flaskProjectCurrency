import json
import pandas as pd
import requests

from pymongo import MongoClient
from main_folder.models import Currency

client = MongoClient('localhost', 27017)
db = client['currency_db']


def create_curr(currency_code, code, name, rate):
    curr = Currency(
        currency_code=currency_code,
        code=code,
        name=name,
        rate=rate)
    curr.save()


def get_data_from_app():
    res = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')
    response = json.loads(res.text)
    df = pd.DataFrame(response)
    for index, row in df.iterrows():
        currency_code = row['r030']
        code = row['cc']
        name = row['txt']
        rate = row['rate']
        create_curr(currency_code, code, name, rate)
