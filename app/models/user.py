# -*- coding: UTF-8 -*-
from app import db
from flask import jsonify
class User(db.Model):
    __tablename__="user"

    student_number = db.Column(db.String(11),primary_key=True)
    nickname = db.Column(db.String(100))
    sex = db.Column(db.String(5))
    phone_number = db.Column(db.String(15))
    signature = db.Column(db.String(250))
    head_portrait = db.Column(db.BLOB)
    password = db.Column(db.String(250))
    be_attention_number = db.Column(db.Integer)


    def __init__(self,student_number,password):
        self.student_number = student_number
        self.password = password
        self.be_attention_number = 0


    def get_info(self):
        data = {
            "nickname": self.nickname,
            "phone_number": self.phone_number,
            "sex": self.sex,
            "signature": self.signature,
            "head_portrait": self.head_portrait,
            "student_number": self.student_number,
            "be_attention_number": self.be_attention_number
        }
        return data

    def get_simple_info(self):
        data = {"nickname": self.nickname,
                "sex": self.sex,
                "head_portrait": self.head_portrait,
                "signature": self.signature
                }
        return data


def query_user(id):
    one = User.query.filter_by(student_number=id).first()
    return one

def session_commit():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(falseReturn("数据库连接失败"))






