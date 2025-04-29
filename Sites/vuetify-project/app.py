from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, HTTPException, Depends, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from flask import Flask, request, jsonify
from flask_cors import CORS

app = FastAPI()
app = Flask(__name__)
CORS(app, resources={
    r"/auth": {
        "origins": "https://localhost:3000",
        "supports_credentials": True
    }
})

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', backref='role_ref', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    nickname = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

@app.route('/auth', methods=['POST', 'OPTIONS'])
def auth():
    if request.method == 'OPTIONS':
        # Обработка предварительного OPTIONS запроса
        return jsonify({}), 200
    
    data = request.get_json()
    # Ваша логика аутентификации...
    return jsonify({
        "token": "example-token",
        "user": data.get('nickName')
    })

if __name__ == '__main__':
    app.run(port=8000, debug=True)