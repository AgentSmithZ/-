from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, Users, Auth, Reviews, Skills, Type
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'IMNDE93M9MSDIOCMmdkf9e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horus.db'

db.init_app(app)

@app.route('/')
@app.route('/home')
def home():
    title = "This my"
    return render_template('home.html', title=title)

@app.route('/table')
def table():
    title = "Table"
    return render_template('table.html', title=title)

@app.route('/image')
def image():
    title = "123321"
    return render_template('image.html', title=title)

@app.route('/listin')
def listin():
    title = "Score"
    score = ['11111','222222','333333','444444']
    return render_template('listin.html', score=score, title=title)


@app.route('/text')
def text():
    title = "jsd"
    text = "Hello"
    return render_template('text.html', text=text, title=title)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = Users.query.filter_by(username=username).first()
        if users and check_password_hash(users.password, password):
            session[Users.id] = users.id
            return redirect(url_for('/home'))
        else:
            flash('Invalid username or password')
        return render_template('auth.html')

def new_func():
    email = request.form['email']
 
@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run()