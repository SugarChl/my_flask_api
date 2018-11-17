from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from app.common import trueReturn, true_data_Return, falseReturn, create_id
from app.auth import login_check, current_user
from app.models.attention import Attention, query_attention, query_all_attention
from app.models.user import query_user
from app.models.user import User
from app import db
from app.models.user import User
attention = Blueprint("attention", __name__)
api_attention = Api(attention)


class Attentionx(Resource):
    @login_check
    def post(self):
        try:
            be_attention_student_number = request.form['be_attention_student_number']
        except:
            return jsonify(falseReturn("缺少部分必要信息"))
        user = current_user()
        id = create_id()
        new = Attention(user.student_number, id, be_attention_student_number)
        db.session.add(new)
        session_commit()
        be_attention_user = User.query.filter_by(student_number=be_attention_student_number).first()
        be_attention_user.be_attention_number += 1
        session_commit()
        return jsonify(trueReturn("关注成功"))

    @login_check
    def delete(self):
        user = current_user()
        try:
            attention_id = request.form['attention_id']
        except:
            return jsonify(falseReturn("缺少部分必要信息"))

        get_one = query_attention(attention_id)
        if user.student_number != get_one.student_number:
            return jsonify(falseReturn("非法删除"))
        if get_one is None:
            return jsonify(falseReturn("不存在该数据"))
        Attention.delete_attention(get_one)
        return jsonify(trueReturn("取消关注成功"))


class AttentionList(Resource):
    @login_check
    def get(self):
        user = current_user()
        my_attention = query_all_attention(user.student_number)
        result = []
        result_number = len(my_attention)
        for i in my_attention:
            user = query_user(i.be_attention_student_number)
            data = User.get_simple_info(user)
            result.append(data)
        return jsonify(true_data_Return([result_number, result], "", "成功获取我的关注"))

def session_commit():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(falseReturn("数据库连接失败"))

api_attention.add_resource(Attentionx, "/")
api_attention.add_resource(AttentionList, "/my_list")