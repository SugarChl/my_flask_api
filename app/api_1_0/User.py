from flask import Blueprint
from flask import request, jsonify
from flask_restful import Api, Resource
from app.models.user import User
from app.auth import generate_auth_token, current_user, login_to_fzu
from app import db
from app.auth import login_check
from app.common import trueReturn, falseReturn, true_data_Return
user = Blueprint("user", __name__)
api_user = Api(user)


class User_info(Resource):
    @login_check
    def get(self):
        user = current_user()
        data = User.get_info(user)
        return jsonify(true_data_Return(data,"null","获取用户信息成功"))


    @login_check
    def put(self):
        try:
            signature = request.form['signature']
            phone_number = request.form['phone_number']
            sex = request.form['sex']
            nickname = request.form['nickname']
        except:
            return jsonify(falseReturn("缺少部分个人信息"))
        user = current_user()
        user.signature = signature
        user.sex = sex
        user.phone_number = phone_number
        user.nickname = nickname
        db.session.commit()
        return jsonify(trueReturn("更新个人信息成功"))


class User_login(Resource):
    def post(self):
        student_number = request.form['student_number']
        password = request.form['password']
        if login_to_fzu(student_number, password):
            token = generate_auth_token(student_number)
            user = User.query.filter_by(student_number=student_number).first()
            if user is None:
                new = User(student_number=student_number, password=password)
                db.session.add(new)
                session_commit()
            return jsonify(true_data_Return("null", token, "登录成功"))
        else:
            return jsonify(falseReturn("登录失败，用户名或密码错误"))



class User_register(Resource):
    def post(self):
        pass


def session_commit():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(falseReturn("数据库连接失败"))

api_user.add_resource(User_info, "/info")
api_user.add_resource(User_login, "/login")