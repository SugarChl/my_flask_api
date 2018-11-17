from app import db
from flask import jsonify
class Attention(db.Model):
    __tablename__ = "attention"

    student_number = db.Column(db.String(15))
    attention_id = db.Column(db.String(15),primary_key=True)
    be_attention_student_number = db.Column(db.String(15))

    def __init__(self, student_number, attention_id, be_attention_student_number):
        self.student_number = student_number
        self.attention_id = attention_id
        self.be_attention_student_number = be_attention_student_number

    def delete_attention(self):
        self.query.filter_by(attention_id=self.attention_id).delete()
        return session_commit()


def query_attention(id):
    get_one = Attention.query.filter_by(attention_id=id).first()
    return get_one

def query_all_attention(id):
    get = Attention.query.filter_by(student_number=id).all()
    return get

def session_commit():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(falseReturn("数据库连接失败"))