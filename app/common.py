from app.__init__ import db
from flask import jsonify
import time

def true_data_Return(data, token, msg):
    return {
        "status": True,
        "data": data,
        "token": token,
        "msg": msg
    }

def trueReturn(msg):
    return {
        "status": True,
        "msg": msg
    }

def falseReturn(msg):
    return {
        "status": False,
        "msg": msg
    }




def create_id():
    return str(int(time.time()))
