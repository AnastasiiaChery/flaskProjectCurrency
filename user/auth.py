from flask import Blueprint, jsonify, request, redirect
from flask_login import login_user, logout_user

from datetime import datetime, timedelta
import bcrypt as bcrypt
import jwt

from . import login_manager
from .models import User

auth = Blueprint('auth', __name__)


JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 200


@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password').encode('utf-8')
    user = User.objects(email=email).first()

    if bcrypt.checkpw(password, user.password.encode('utf-8')):
        login_user(user)
        return get_token(user)
    else:
        return jsonify({"status": 401,
                        "reason": "Username or Password Error"})


def get_token(user):
    payload = {
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

    return jsonify({'token': jwt_token})


@auth.route("/logout")
@login_manager.user_loader
def logout():
    logout_user()
    return redirect('/')


@auth.route('/signup', methods=['POST'])
def create_record():
    create_user(request.form.get('email'), request.form.get('password'),  request.form.get('name'), request.form.get('surname'))
    return 'created successfully'

def create_user(email, password, name, surname):
    user = User(
        email=email,
        password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
        name=name,
        surname=surname)
    user.save()

