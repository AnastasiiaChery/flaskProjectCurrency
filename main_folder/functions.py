import datetime
import pandas as pd

from pymongo import MongoClient
from . import db

# Connect to mongo db

client = MongoClient('localhost', 27017)
db = client['currency_db']


# Change base currency
def base_currency(curr_id, list_curr):
    df = pd.DataFrame(list_curr)
    base_rate = ''
    new_list = []
    for index, row in df.iterrows():

        if row['code'] == curr_id.upper():
            base_rate = row['rate']
    for index, row in df.iterrows():
        row['rate'] = row['rate'] / base_rate
        new_list.append(dict(row))
    return new_list


# Select a list of currencies by date
def data_filter(selected_date):
    if selected_date:
        list_currency = []

        s_datetime = datetime.datetime.strptime(selected_date, '%Y%m%d')
        next_datetime = s_datetime + datetime.timedelta(days=1)

        for curr in db.currency.find({"date": {'$gte': s_datetime,
                                               '$lt': next_datetime}}, {'_id': 0}):
            list_currency.append(curr)
    else:
        list_currency = []
        for curr in db.currency.find({}, {'_id': 0}).sort("date", -1).limit(60):
            list_currency.append(curr)

    return list_currency


# Select a list of currencies for the period
def curr_hisrory(st_date, ls_date):
    st_date = datetime.datetime.strptime(st_date, '%Y%m%d')
    ls_date = datetime.datetime.strptime(ls_date, '%Y%m%d')
    list_currency = []
    for curr in db.currency.find({"date": {'$gte': st_date, '$lt': ls_date}}, {'_id': 0}):
        list_currency.append(curr)
    return list_currency


# Select columns rate and currency
def selected_df(curr_list):
    curr_list_df = pd.DataFrame(curr_list)
    selected_df = curr_list_df[['rate', 'code']]
    return selected_df


# Min
def curr_min(curr_list):
    ls = selected_df(curr_list)
    min_list = ls.groupby('code').min()
    return min_list


# Max
def curr_max(curr_list):
    ls = selected_df(curr_list)
    mean_list = ls.groupby('code').max()
    return mean_list


# Mean
def curr_mean(curr_list):
    ls = selected_df(curr_list)
    mean_list = ls.groupby('code').mean()
    return mean_list


# Converter
def converter(new_list, from_curr, selected_sum):
    for i in new_list:
        if i['code'] == from_curr:
            output = float(selected_sum) * float(i['rate'])
    return output
