import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(80), nullable=False, unique=True)
    # comma separated choices.
    choices = db.Column(db.String(160), nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)

    def get_choices(self):
        return json.loads(self.choices)

    def set_choices(self, choices):
        self.choices = json.dumps(choices)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    questions = db.relationship("Question", backref="quiz", lazy=True)
