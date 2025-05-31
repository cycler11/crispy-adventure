from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from app import bcrypt

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('books.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('books.index'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('books.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует', 'danger')
        else:
            user = User(username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Пользователь успешно зарегистрирован', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')