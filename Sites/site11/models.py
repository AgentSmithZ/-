from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask import Flask
from datetime import datetime

app = Flask (__name__)

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horus.db'

db = SQLAlchemy()
db.init_app(app)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Активен')
    is_active = db.Column(db.Boolean, default=True)

class Shifts(db.Model):
    __tablename__ = 'shifts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    waiters = db.Column(db.String(200), nullable=False)
    cook = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)
    orders = relationship('Order', back_populates="shift")

class MenuItem(db.Model):
    __tablename__ = 'menuitem'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'food', 'drink'
    is_available = db.Column(db.Boolean, default=True)

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, nullable=False)
    customer_count = db.Column(db.Integer, nullable=False)
    items = db.Column(db.String(255), nullable=False)  # Список заказанных блюд и напитков
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Принят')
    shift_id = db.Column(db.Integer, ForeignKey('shifts.id'))

    shift = relationship("Shifts", back_populates="orders")

class OrderItem(db.Model):
    __tablename__ = 'orderitem'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menuitem.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.Text)

#def add_user(username, password, role):
    #new_user = Users(username=username, password=password, role=role)
    #db.session.add(new_user)
    #db.session.commit()

#with app.app_context():
    #db.create_all()
    #db.session.commit()

    #add_user(username='admin', password=123456, role='Admin')
    #add_user(username='waiter', password=123456, role='Waiter')
    #add_user(username='cook', password=123456, role='Cook')
