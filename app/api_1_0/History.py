from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import time
from app.auth import verify_auth_token
from app.auth import current_user, login_check

from app.common import trueReturn, true_data_Return, falseReturn
from app.models.history import History, query_history, query_all_history
from app.__init__ import db
history = Blueprint("history", __name__)
api_history = Api(history)


class Historyx(Resource):
    @login_check
    def delete(self, id):
        user = current_user()
        h = query_history(user.student_number, id)
        if h is None:
            return jsonify(true_data_Return("null", "null", "无数据"))

        History.delete_h(h)

        return jsonify(trueReturn("删除历史记录成功"))

class HistoryList(Resource):

    @login_check
    def get(self, student_number):
        h = query_all_history(student_number)
        if h is None:
            return jsonify(true_data_Return("null", "null", "无数据"))
        data=[]
        for i in h:
            data.append(History.get(i))
        return jsonify(true_data_Return(data, "", "获取数据成功"))

    @login_check
    def delete(self, student_number):
        user = current_user()
        h = query_all_history(student_number)
        if h is None:
            return jsonify(true_data_Return("null", "null", "无数据"))
        for i in h:
            if i.student_number != user.student_number:
                return jsonify(falseReturn("非法删除,错误"))
            else:
                History.delete_h(i)

        return jsonify(trueReturn("删除历史记录成功"))





api_history.add_resource(Historyx, "/delete/id=<string:id>")
api_history.add_resource(HistoryList, "/historylist/student_number=<string:student_number>")