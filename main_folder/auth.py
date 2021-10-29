from datetime import datetime, timedelta

import bcrypt as bcrypt
import jwt
from flask import Blueprint, jsonify, request, make_response

from .models import User, BlackJWTList

auth = Blueprint('auth', __name__)

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 200


#####Create user
@auth.route('/signup', methods=['POST'])
def create_record():
    create_user(request.form.get('email'), request.form.get('password'), request.form.get('name'),
                request.form.get('surname'))
    return 'created successfully'


def create_user(email, password, name, surname):
    user = User(
        email=email,
        password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
        name=name,
        surname=surname)
    user.save()


#####Login
@auth.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.objects(email=auth.username).first()

    if bcrypt.checkpw(auth.password.encode('utf-8'), user.password.encode('utf-8')):
        token = jwt.encode(
            {'email': user.email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, JWT_SECRET, JWT_ALGORITHM)
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


#####Logout
@auth.route('/logout', methods=['POST'])
def logout():
    token = request.headers['x-access-tokens']
    black_list_token = BlackJWTList(
        data=token)
    black_list_token.save()
    return jsonify({"msg": "Successfully logged out"}), 200
