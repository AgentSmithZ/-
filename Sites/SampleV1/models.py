from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
#from flask import Flask

#app = Flask (__name__)

#app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horus.db'

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    users_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    register_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    id_auth = db.Column(db.Integer, db.ForeignKey('auth.id'))

class Auth(db.Model, UserMixin):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Projects(db.Model, UserMixin):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    id_reviews = db.Column(db.Integer, db.ForeignKey('reviews.id'))
    url = db.Column(db.String(100), nullable=True)

class Reviews(db.Model, UserMixin):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_reviews = db.Column(db.String(100), unique=True, nullable=False)
    feedback = db.Column(db.String(255), nullable=False)

class Skills(db.Model, UserMixin):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    name = db.Column(db.String(100), unique=True, nullable=False)
    id_type = db.Column(db.Integer, db.ForeignKey('type.id'))

class Type(db.Model, UserMixin):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


#with app.app_context():
    #db.create_all()
    #db.session.commit()
