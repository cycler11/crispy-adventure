from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from models import User, Book
    with app.app_context():
        db.create_all()

    from auth.routes import auth_bp
    from books.routes import books_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(books_bp, url_prefix='/books')

    @app.route('/')
    def index():
        return '<h1>Библиотека</h1><p><a href="/books">Книги</a> | <a href="/auth/login">Войти</a> | <a href="/auth/register">Регистрация</a></p>'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')