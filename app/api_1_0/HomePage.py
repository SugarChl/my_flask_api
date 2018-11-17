from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import time
import random
from app.auth import verify_auth_token
from app.auth import current_user, login_check

from app.common import trueReturn, true_data_Return, falseReturn
from app.models.history import History, query_history, query_all_history
from app.models import Article, Activity
from app.__init__ import db
homepage = Blueprint("homepage", __name__)
api_homepage = Api(homepage)


class HomePage(Resource):
    def get(self, type):
        if type == "activity":
            ac = Activity.query.all()
        elif type == "article":
            ac = Article.query.all()
        data = []
        if len(ac) < 20:
            for i in range(len(ac)):
                x = Activity.get_activities(ac[i])
                data.append(x)
        else:
            ten_ac = random.sample(ac, 20)
            for i in range(len(ten_ac)):
                x = Activity.get_activities(ten_ac[i])
                data.append(x)

        return jsonify(true_data_Return(data, "", "获取数据成功"))


api_homepage.add_resource(HomePage, "/type=<string:type>")