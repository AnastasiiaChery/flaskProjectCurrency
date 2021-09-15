import datetime
import json



import jwt
import pandas as pd
import requests
import schedule
import time
from aiohttp import web
from flask import Blueprint, render_template, jsonify, request
from . import db
from .auth import JWT_SECRET, JWT_ALGORITHM
from .models import User, Currency
from pymongo import MongoClient

main = Blueprint('main', __name__)

# Подключение к БД и таблице
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['currency_db']



@main.route('/')
def home_page():
    result = list_curr()

    return jsonify(str(result))


def list_curr():
    list_currency = []
    for curr in db.currency.find({}, {'_id': 0}).sort("date", -1).limit(60):
        list_currency.append(curr)

    return list_currency



@main.route('/<string:curr_id>')
def change_base_currency(curr_id):
    result = list_curr()
    df = pd.DataFrame(result)
    base_rate = ''
    new_list=[]
    for index, row in df.iterrows():
        print(row)
        if row['code'] == curr_id.upper():
            base_rate=row['rate']
    for index, row in df.iterrows():
        print(row['rate'])
        print(base_rate)
        row['rate']=row['rate']/base_rate
        new_list.append(dict(row))
    return jsonify(str(new_list))


# ???????????????????
@main.route('/by_date', methods=['POST'])
def select_currency_by_data():
    list_currency=[]
    selected_date = request.form.get('date')
    s_datetime = datetime.datetime.strptime(selected_date, '%Y%m%d')
    result = s_datetime.strftime("%Y, %m, %d, %H, %M")
    print(result)
    # date_time= datetime.datetime(s_datetime)
    print(s_datetime)
    # print(date_time)

    for curr in db.currency.find({"date":datetime.datetime(2022, 9, 13)}, {'_id': 0}):
        print(curr)
    # for curr in db.currency.find({"date": datetime.datetime(s_datetime)}, {'_id': 0}):
        list_currency.append(curr)

    return jsonify(str(list_currency))
    # return 'list_currency'


@main.route('/profile', methods=['POST'])
def profile():
    encoded_jwt = request.form.get('encoded_jwt')
    data = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    print(data)
    return data


def create_curr(currency_code, code, name, rate):
    curr = Currency(
        currency_code=currency_code,
        code=code,
        name=name,
        rate=rate)
    curr.save()


def get_data():
    res = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')
    response = json.loads(res.text)
    df = pd.DataFrame(response)
    for index, row in df.iterrows():
        currency_code = row['r030']
        code = row['cc']
        name = row['txt']
        rate = row['rate']
        create_curr(currency_code, code, name, rate)

#
# schedule.every().day.at("16:56").do(get_data)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
