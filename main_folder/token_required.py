from functools import wraps
import jwt
from flask import jsonify, request
from .auth import JWT_SECRET, JWT_ALGORITHM
from .models import User, BlackJWTList


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        for i in BlackJWTList.objects():
            if token == i['data']:
                return jsonify({'message': 'User is not logged in'})

        try:
            data = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
            current_user = User.objects(email=data['email']).get()

        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator
