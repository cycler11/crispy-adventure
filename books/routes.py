from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from models import Book

books_bp = Blueprint('books', __name__, template_folder='templates')

@books_bp.route('/')
@login_required
def index():
    books = Book.query.all()
    return render_template('books/index.html', books=books)

@books_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role not in ['admin', 'librarian']:
        return "Доступ запрещён", 403
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = int(request.form['year'])
        book = Book(title=title, author=author, year=year)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.index'))
    return render_template('books/create.html')

@books_bp.route('/<int:id>')
@login_required
def detail(id):
    book = Book.query.get_or_404(id)
    return render_template('books/detail.html', book=book)