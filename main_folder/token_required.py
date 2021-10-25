from functools import wraps
import jwt
from flask import jsonify, request
from .auth import JWT_SECRET, JWT_ALGORITHM
from .models import User


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            # print(jwt.decode(token, JWT_SECRET, JWT_ALGORITHM))
            data = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
            current_user = User.objects(email=data['email']).first()

        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator