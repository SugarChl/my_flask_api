from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import time
from app.config import Config
from app.models.user import User
from functools import wraps
import requests
from bs4 import BeautifulSoup
from app.common import falseReturn, trueReturn
from flask import request, jsonify

def generate_auth_token(student_number):
    s = Serializer(
        secret_key=Config.SECRET_KEY,
        expires_in=50000)
    timestamp = time.time()
    return str(s.dumps(
        {'user_id': student_number,
         'iat': timestamp}),encoding="utf-8")



def login_check(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.form['token']
        if not token:
            return jsonify(falseReturn("需要token验证"))
        a_user = verify_auth_token(token)
        if a_user is None:
            return jsonify(falseReturn("非法token，请重新登录"))

        return f(*args, **kwargs)

    return decorator


def verify_auth_token(token):
    s = Serializer(Config.SECRET_KEY)
    try:
        data = s.loads(token)
    except:
        return None  # invalid token
    user = User.query.filter_by(student_number=data['user_id']).first()
    return user

def current_user():
    token = request.form['token']
    user = verify_auth_token(token)
    return user

def login_to_fzu(student_number, password):
    url = "http://59.77.226.32/logincheck.asp"
    data = {"muser": student_number, "passwd": password}
    x = requests.post(url, data=data)
    ss = BeautifulSoup(x.text, 'lxml')
    body = ss.find('body')
    if body is not None:
        return True
    else:
        return False