from app import db
from flask import jsonify
from app.auth import current_user
import time
from app.common import falseReturn
class History(db.Model):
    __tablename__ = "history"

    time = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(50))
    student_number = db.Column(db.String(20))
    something_id = db.Column(db.String(20))
    type = db.Column(db.String(20))

    def __init__(self,time,title,student_number,something_id,type):
        self.student_number = student_number
        self.time = time
        self.title = title
        self.type = type
        self.something_id = something_id

    def get(self):
        data ={
            "title":self.title,
            "time":self.time,
            "type":self.type,
            "id":self.something_id
        }
        return data

    def delete_h(self):
        self.query.filter_by(time=self.time).delete()
        return session_commit()

def query_history(student_number, id):
    l = History.query.filter_by(student_number=student_number).filter_by(something_id=id).first()
    return l

def query_all_history(student_number):
    l = History.query.filter_by(student_number=student_number).all()
    return l

def history(type, title, id):
    student_number = current_user().student_number
    t = str(int(time.time()))
    new = History(t, title, student_number, id, type)
    db.session.add(new)
    session_commit()

def session_commit():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(falseReturn("数据库连接失败"))