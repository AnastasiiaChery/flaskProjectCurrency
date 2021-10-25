from flask import Blueprint, jsonify, request
from flask_login import login_required


from main_folder.functions import data_filter, base_currency, curr_hisrory, curr_min, curr_max, curr_mean, converter
from main_folder.token_required import token_required

main = Blueprint('main', __name__)


# Returns a list of all currencies for the current date

@main.route('/')
@token_required
def home_page(*args, **kwargs):

    list_curr = data_filter(request.form.get('date'))

    return jsonify(list_curr)


# Returns a list of all currencies for the selected date
@main.route('/by_date', methods=['POST'])
@token_required
def select_currency_by_data(*args, **kwargs):
    list_curr = data_filter(request.form.get('date'))
    return jsonify(list_curr)


# Returns a list of currencies. The base currency changes. By default, for the current date, but
# if the date parameter is specified, for the selected
@main.route('/select', methods=['POST'])
@token_required
def change_base_currency(*args, **kwargs):
    list_curr = data_filter(request.form.get('date'))
    curr_id= request.form.get('curr_id')
    new_list = base_currency(curr_id, list_curr)
    return jsonify(new_list)


#Mean, minimum, maximum. Period from ... to. If the currency code is not specified,
# the entire list is returned. If specified, one currency.

@main.route('/characteristic', methods=['POST'])
@token_required
def currency_characteristic(*args, **kwargs):
    curr_list = curr_hisrory(request.form.get('st_date'), request.form.get('ls_date'))
    strategy = {
        'min': curr_min,
        'max': curr_max,
        'mean': curr_mean
    }
    action = request.form.get('action')
    summary = strategy[action](curr_list)

    result = summary.to_dict()['rate']

    curr_code = request.form.get('code')
    if not curr_code:
        return jsonify(result)

    return jsonify(result[curr_code])


# Currency Converter
@main.route('/currency-converter', methods=['POST'])
@token_required
def currency_converter(*args, **kwargs):
    list_curr = data_filter(request.form.get('date'))
    new_list = base_currency(request.form.get('to'), list_curr)
    converted_sum = converter(new_list, request.form.get('from'), request.form.get('sum'))

    return jsonify(converted_sum)




