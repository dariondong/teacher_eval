from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ClassConfig(db.Model):
    __tablename__ = 'class_config'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(10), unique=True, nullable=False)
    class_count = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @staticmethod
    def get_count(grade):
        cfg = ClassConfig.query.filter_by(grade=grade).first()
        return cfg.class_count if cfg else 0

    @staticmethod
    def get_all_as_dict():
        configs = ClassConfig.query.all()
        return {c.grade: c.class_count for c in configs}


class QuestionConfig(db.Model):
    __tablename__ = 'question_config'
    id = db.Column(db.Integer, primary_key=True)
    question_number = db.Column(db.Integer, unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    max_score = db.Column(db.Integer, nullable=False, default=5)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Evaluation(db.Model):
    __tablename__ = 'evaluation'

    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(10), nullable=False)
    class_name = db.Column(db.String(10), nullable=False)
    teacher_subject = db.Column(db.String(20), nullable=False)

    q1 = db.Column(db.String(1), nullable=False)
    q2 = db.Column(db.String(1), nullable=False)
    q3 = db.Column(db.String(1), nullable=False)
    q4 = db.Column(db.String(1), nullable=False)
    q5 = db.Column(db.String(1), nullable=False)
    q6 = db.Column(db.String(1), nullable=False)
    q7 = db.Column(db.String(1), nullable=False)
    q8 = db.Column(db.String(1), nullable=False)
    q9 = db.Column(db.String(1), nullable=False)
    q10 = db.Column(db.String(1), nullable=False)
    q11 = db.Column(db.String(1), nullable=False)
    q12 = db.Column(db.String(1), nullable=False)
    q13 = db.Column(db.String(1), nullable=False)
    q14 = db.Column(db.String(1), nullable=False)
    q15 = db.Column(db.String(1), nullable=False)
    q16 = db.Column(db.String(1), nullable=False)
    q17 = db.Column(db.String(1), nullable=False)
    q18 = db.Column(db.String(1), nullable=False)
    q19 = db.Column(db.String(1), nullable=False)
    q20 = db.Column(db.String(1), nullable=False)

    device_uuid = db.Column(db.String(36), nullable=True, index=True)

    suggestions = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    ip_address = db.Column(db.String(50), default='')

    def score_of(self, q):
        score_map = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1}
        val = getattr(self, q, 'C')
        return score_map.get(val, 3)

    @property
    def total_score(self):
        return sum(self.score_of(f'q{i}') for i in range(1, 21))

    @property
    def average_score(self):
        return round(self.total_score / 20, 2)

    def to_dict(self):
        return {
            'id': self.id,
            'grade': self.grade,
            'class_name': self.class_name,
            'teacher_subject': self.teacher_subject,
            'total_score': self.total_score,
            'average_score': self.average_score,
            'suggestions': self.suggestions,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
        }
