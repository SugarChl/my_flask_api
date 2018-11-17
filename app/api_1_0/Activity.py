from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
import time
from app.models.activity import Activity, query_activity, query_someone_activity
from app.auth import login_check, current_user
from app.common import true_data_Return, falseReturn, trueReturn, create_id
from app import db
from app.models.history import history
activity = Blueprint("activity", __name__)
api_activity = Api(activity)


class Activityx(Resource):
    @login_check
    def get(self, id):
        activity = query_activity(id)
        if activity is None:
            return jsonify(falseReturn("该活动不存在"))
        data = []
        data.append(Activity.get_activities(activity))
        history("activity", activity.title, id)
        return jsonify(true_data_Return(data, "", "获取数据成功"))


    @login_check
    def delete(self, id):
        user = current_user()
        activity = query_activity(id)
        if activity is None:
            return jsonify(falseReturn("该活动不存在"))
        if activity.sponsor_student_number != user.student_number:
            return jsonify(falseReturn("非法删除，只有该活动的作者才可以删除该活动"))
        Activity.delete_activity(activity)
        return jsonify(trueReturn("删除活动成功"))

    @login_check
    def put(self, id):
        user = current_user()
        activity = query_activity(id)
        if activity is None:
            return jsonify(falseReturn("该活动不存在"))
        if activity.sponsor_student_number != user.student_number:
            return jsonify(falseReturn("非法篡改"))
        try:
            title = request.form['title']
            bt = request.form['begin_time']
            et = request.form['end_time']
            content = request.form['content']
        except:
            return jsonify(falseReturn("缺少部分必要信息"))
        try:
            begin_time = int(time.mktime(time.strptime(bt, "%Y-%m-%d %H:%M:%S")))
            end_time = int(time.mktime(time.strptime(et, "%Y-%m-%d %H:%M:%S")))
        except:
            return jsonify(falseReturn("时间格式错误"))
        activity.title = title
        activity.content = content
        activity.begin_time = begin_time
        activity.end_time = end_time
        session_commit()
        return jsonify(trueReturn("修改文章成功"))

class New_activity(Resource):
    @login_check
    def post(self):
        user = current_user()
        try:
            title = request.form['title']
            bt = request.form['begin_time']
            et = request.form['end_time']
            content = request.form['content']
        except:
            return jsonify(falseReturn("缺少必要信息"))
        try:
            begin_time = int(time.mktime(time.strptime(bt, "%Y-%m-%d %H:%M:%S")))
            end_time = int(time.mktime(time.strptime(et, "%Y-%m-%d %H:%M:%S")))
        except:
            return jsonify(falseReturn("时间格式错误"))
        activity_id = create_id()
        sponsor_student_number = user.student_number
        new = Activity(title, begin_time, end_time, activity_id, sponsor_student_number, content)
        db.session.add(new)
        session_commit()
        return jsonify(trueReturn("创建活动成功"))


class Activity_list(Resource):
    @login_check
    def get(self, student_number):
        activities = query_someone_activity(student_number)
        if activities is None:
            return jsonify(true_data_Return("null", "null", "无数据"))
        data = []
        for i in activities:
            data.append(Activity.get_simple_activity(i))
        return jsonify(true_data_Return(data, "", "获取数据成功"))

def session_commit():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(falseReturn("数据库连接失败"))

api_activity.add_resource(Activityx, "/activity_id=<string:id>")
api_activity.add_resource(Activity_list, "/list/student_number=<string:student_number>")
api_activity.add_resource(New_activity, "/new_activity")