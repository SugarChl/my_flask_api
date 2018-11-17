from flask import Blueprint
from flask import request, jsonify
from flask_restful import Api, Resource
from app.models.user import User
from app.auth import generate_auth_token, current_user, login_to_fzu
from app import db
from app.auth import login_check
from app.common import trueReturn, falseReturn, true_data_Return
from app.models.article import Article
from app.models.activity import Activity
search = Blueprint("search", __name__)
api_search = Api(search)

class Search(Resource):
    def get(self, keyword):
        activities = Activity.query.filter(Activity.title.ilike('%' + keyword + '%')).all()
        articles = Article.query.filter(Article.title.ilike('%' + keyword + '%')).all()
        result = []
        for i in range(len(articles)):
            a = Article.get_simple_article(articles[i])
            result.append(a)

        for i in range(len(activities)):
            a = Activity.get_simple_activity(activities[i])
            result.append(a)
        result_number = len(activities)+len(articles)
        data=[result_number, result]
        print(data)
        return jsonify(true_data_Return(data, "", "获取数据成功"))

api_search.add_resource(Search, "/keyword=<string:keyword>")