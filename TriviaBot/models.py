from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True
    )

    email = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(
        db.String(200)
    )

    score = db.Column(
        db.Integer,
        default=0
    )



class QuizHistory(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer
    )

    question = db.Column(
        db.String(300)
    )

    correct = db.Column(
        db.String(200)
    )

    answer = db.Column(
        db.String(200)
    )
