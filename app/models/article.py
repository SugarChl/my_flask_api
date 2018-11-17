from app import db
from flask import jsonify

class Article(db.Model):
    __tablename__ = "article"

    title = db.Column(db.String(50))
    writer_student_number = db.Column(db.String(20), primary_key=True)
    article_id = db.Column(db.String(20), primary_key=True)
    content = db.Column(db.TEXT)

    def __init__(self, title, writer_student_number, article_id,content):
        self.title=title
        self.writer_student_number=writer_student_number
        self.article_id=article_id
        self.content=content

    def get_article(self):
        data={"title":self.title,
              "article_id":self.article_id,
              "content":self.content,
              "type":"article"}
        return data

    def get_simple_article(self):
        data = {"title": self.title,
                "article_id": self.article_id,
                "type": "article"}
        return data


    def delete_article(self):
        self.query.filter_by(article_id=self.article_id).delete()
        return session_commit()


def query_someone_article(student_id):
    articles = Article.query.filter_by(writer_student_number=student_id).all()
    return articles

def query_article(article_id):
    article = Article.query.filter_by(article_id=article_id).first()
    return article

def session_commit():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(falseReturn("数据库连接失败"))