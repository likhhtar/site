from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.String(150))
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    times = db.relationship('Time')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    second_name = db.Column(db.String(150))
    notes = db.relationship('Note')

