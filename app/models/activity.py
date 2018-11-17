from app import db
from flask import jsonify
class Activity(db.Model):
    __tablename__="activity"


    title = db.Column(db.String(50))
    begin_time = db.Column(db.String(20))
    end_time = db.Column(db.String(20))
    activity_id = db.Column(db.String(20),primary_key=True)
    be_attention_number = db.Column(db.Integer)
    sponsor_student_number = db.Column(db.String(20))
    content = db.Column(db.TEXT)

    def __init__(self, title, begin_time, end_time, activity_id, sponsor_student_number, content):
        self.be_attention_number = 1
        self.content = content
        self.title = title
        self.activity_id = activity_id
        self.begin_time = begin_time
        self.end_time = end_time
        self.sponsor_student_number = sponsor_student_number

    def get_activities(self):
        data={"title":self.title,
              "activity_id":self.activity_id,
              "content":self.content,
              "begin_time":self.begin_time,
              "end_time":self.end_time,
              "be_attention_number":self.be_attention_number,
              "type":"activity"}
        return data

    def get_simple_activity(self):
        data = {"title": self.title,
                "article_id": self.activity_id,
                "begin_time": self.begin_time,
                "end_time": self.end_time,
                "be_attention_number": self.be_attention_number,
                "type": "activity"}
        return data


    def delete_activity(self):
        self.query.filter_by(activity_id=self.activity_id).delete()
        session_commit()



def query_someone_activity(student_id):
    activities = Activity.query.filter_by(sponsor_student_number=student_id).all()
    return activities

def query_activity(activity_id):
    activity = Activity.query.filter_by(activity_id=activity_id).first()
    return activity


def session_commit():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(falseReturn("数据库连接失败"))