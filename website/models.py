from flask_login import UserMixin
from .utils import db
from sqlalchemy.sql import func
from datetime import datetime
from uuid import uuid4

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(length=60), nullable=False,  unique=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    urls = db.relationship('URL', backref='user', lazy=True)
    confirm =  db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"


    def save(self):
        self.uuid = uuid4().hex
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
   
    


class URL(db.Model):
    __tablename__ = 'url'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    original_url = db.Column(db.String(2000), nullable=False)
    short_url = db.Column(db.String(6), unique=True, nullable=False)
    custom_url = db.Column(db.String(6))
    users = db.Column(db.Integer(), db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    visitors = db.Column(db.Integer(), default = 0)

    def __init__(self, original_url, short_url, custom_url, users, name):
        self.original_url = original_url
        self.short_url = short_url
        self.custom_url = custom_url
        self.users = users
        self.name = name
    
    def save(self):
        self.uuid = uuid4().hex
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


