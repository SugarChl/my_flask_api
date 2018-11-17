from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from app.models.article import Article, query_someone_article, query_article
from app.common import trueReturn, true_data_Return, falseReturn, create_id
from app.auth import login_check, current_user
from app.models.user import User
from app.models.article import Article
from app import db
from app.models.history import history
article = Blueprint("article", __name__)
api_article = Api(article)


class Articlex(Resource):
    @login_check
    def get(self, id):
        article = query_article(id)
        if article is None:
            return jsonify(falseReturn("该文章不存在"))
        data = []
        data.append(Article.get_article(article))
        history("article", article.title, id)
        return jsonify(true_data_Return(data, "", "获取数据成功"))

    @login_check
    def put(self, id):
        user = current_user()
        article = query_article(id)
        if article is None:
            return jsonify(falseReturn("该文章不存在"))
        if article.writer_student_number != user.student_number:
            return jsonify(falseReturn("非法篡改"))
        try:
            title = request.form['title']
            content = request.form['content']
        except:
            return jsonify(falseReturn("缺少部分必要信息"))
        print(article.title)
        article.title = title
        article.content = content
        print(article.title)
        db.session.commit()
        return jsonify(trueReturn("修改文章成功"))



    @login_check
    def delete(self, id):
        user = current_user()
        article = query_article(id)
        if article is None:
            return jsonify(falseReturn("该文章不存在"))
        if article.writer_student_number != user.student_number:
            return jsonify(falseReturn("非法删除，只有该文章的作者才可以删除文章"))
        Article.delete_article(article)
        return jsonify(trueReturn("删除文章成功"))

class New_article(Resource):
    @login_check
    def post(self):
        user = current_user()
        try:
            title = request.form['title']
            content = request.form['content']
        except:
            return jsonify(falseReturn("缺少部分必要信息"))
        article_id = create_id()
        new = Article(title, user.student_number, article_id, content)
        db.session.add(new)
        session_commit()
        return jsonify(trueReturn("上传文章成功"))

class Article_List(Resource):
    @login_check
    def get(self, student_number):
        articles = query_someone_article(student_number)
        if articles is None:
            return jsonify(true_data_Return("null", "null", "无数据"))
        data=[]
        for i in articles:
            data.append(Article.get_simple_article(i))
        return jsonify(true_data_Return(data, "", "获取数据成功"))


def session_commit():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(falseReturn("数据库连接失败"))

api_article.add_resource(Articlex, "/detail/article_id=<string:id>")
api_article.add_resource(Article_List, "/list/student_number=<string:student_number>")
api_article.add_resource(New_article, "/new_article")
