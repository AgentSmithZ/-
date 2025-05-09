from flask import Flask, flash, render_template, request, redirect, url_for, session
from models import db, Users, Shifts, Order
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'IMNDE93M9MSDIOCMmdkf9e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horus.db'

db.init_app(app)

@app.route('/')
@app.route('/home')
def home():
    username = session.get('username')
    return render_template('home.html', username=username)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username, password=password).first()
        session['username'] = username
        if user:
            session['username'] = username
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Вы успешно вошли!')
            return redirect(url_for('home'))
        else:
            flash('Неверное имя пользователя или пароль')
    return render_template('auth.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') == 'Admin':
        users = Users.query.all()  
        shifts = Shifts.query.all()
        return render_template('admin/admin_dashboard.html', users=users, shifts=shifts)
    else:
        flash('У вас нет прав для доступа к этой странице.', 'danger')
        return redirect(url_for('home'))

@app.route('/admin/add_employees', methods=['GET', 'POST'])
def add_employees():
    if request.method == 'POST':
        if session.get('role') == 'Admin':  # Проверяем роль
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']

            # Создаем нового пользователя
            new_user = Users(username=username, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()
            flash('Пользователь успешно зарегистрирован!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('У вас нет прав для регистрации пользователей.', 'danger')
            return redirect(url_for('home'))
    return render_template('admin/add_employees.html')

@app.route('/terminate_user/<int:user_id>', methods=['POST'])
def terminate_user(user_id):
    if session.get('role') == 'Admin':  # Проверка роли
        user = Users.query.get(user_id)
        if user:
            user.status = 'уволен'  # Обновляем статус пользователя
            db.session.commit()
            flash(f'Пользователь {user.username} уволен!', 'success')
        else:
            flash('Пользователь не найден.', 'danger')
    else:
        flash('У вас нет прав для выполнения этой операции.', 'danger')
    
    return redirect(url_for('admin_dashboard'))  # Перенаправление на страницу администрирования

@app.route('/admin/schedule_shift', methods=['GET', 'POST'])
def schedule_shift():
    if session.get('role') == 'Admin':  # Проверка роли
        if request.method == 'POST':
            date = request.form['date']
            time = request.form['time']
            waiters = request.form['waiters']  # Официанты через запятую
            cook = request.form['cook']
            date_str = request.form.get('date')

            if not date_str or not time or not waiters or not cook:
                flash('Все поля должны быть заполнены!', 'danger')
                return redirect(url_for('schedule_shift'))

            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Преобразуем строку в объект date
            except ValueError:
                flash('Неверный формат даты!', 'danger')
                return redirect(url_for('schedule_shift'))

            # Создание новой смены
            new_shift = Shifts(date=date, time=time, waiters=waiters, cook=cook)
            db.session.add(new_shift)
            db.session.commit()
            flash('Смена успешно назначена!', 'success')
            return redirect(url_for('admin_dashboard'))

        waiters = Users.query.filter_by(role='Waiter').all()
        cooks = Users.query.filter_by(role='Cook').all()

        return render_template('admin/schedule_shift.html', waiters=waiters, cooks=cooks)
    else:
        flash('У вас нет прав для доступа к этой странице.', 'danger')
        return redirect(url_for('home'))

@app.route('/admin/orders', methods=['GET'])
def view_orders():
    orders = Order.query.all()  # Получаем все заказы из базы данных
    return render_template('admin/view_orders.html', orders=orders)

@app.route('/waiter/orders', methods=['GET'])
def all_orders():
    if session.get('role') in ['Admin', 'Waiter']:  # Доступ для администраторов и официантов
        current_shift_id = get_current_shift_id()  # Функция для получения текущей смены
        orders = Order.query.filter_by(shift_id=current_shift_id).all()
        return render_template('waiter/orders.html', orders=orders)
    else:
        flash('У вас нет прав для доступа к этой странице.', 'danger')
        return redirect(url_for('home'))

@app.route('/waiter/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        table_number = request.form['table_number']
        customer_count = request.form['customer_count']
        items = request.form['items']  # Список блюд и напитков

        new_order = Order(table_number=table_number, customer_count=customer_count, items=items, shift_id=get_current_shift_id())
        db.session.add(new_order)
        db.session.commit()
        flash('Заказ успешно создан!', 'success')
        return redirect(url_for('all_orders'))

    return render_template('waiter/create_order.html')

def get_current_shift_id():
    # Здесь должна быть ваша логика для получения текущей смены
    current_shift = Shifts.query.filter_by(active=True).first()
    return current_shift.id if current_shift else None

@app.route('/cook/orders', methods=['GET'])
def over_orders():
    orders = Order.query.all()  # Получаем все заказы
    return render_template('cook/orders.html', orders=orders)

@app.route('/update_order/<int:order_id>', methods=['POST'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Здесь вы можете добавить логику для изменения статуса заказа.
    # Например, если у вас есть поле статуса в модели заказа:
    new_status = request.form['status']
    
    # Предположим, что у вас есть поле status в модели Order:
    order.status = new_status  # Обновляем статус заказа
    db.session.commit()
    
    return redirect(url_for('over_orders'))

@app.route('/dashboard')
def dashboard():
    return render_template('/dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)  # Удаляем ник пользователя из сессии
    flash('Вы вышли из системы!')
    return redirect(url_for('auth'))
 
@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run()