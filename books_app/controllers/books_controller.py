from flask import render_template, request, redirect 

from books_app.models import authors_model, books_model

from books_app import app

# Books page
@app.route('/books')
def books():
    all_books = books_model.Book.get_all_books()

    if all_books:
        return render_template('books.html', books = all_books)
    else:
        return render_template('books.html')

# Create new book
@app.route('/create_book', methods = ['POST'])
def create_book():
    books_model.Book.create(request.form)

    return redirect('/books')

# View book's favorites
@app.route('/books/<int:id>')
def books_favorites(id):
    results = books_model.Book.get_book_favorites(id)

    authors = authors_model.Author.get_all_authors()

    if results and authors:
        return render_template('books_favorites.html', results = results, authors = authors)
    else:
        return redirect('/')

# Add favorite author
@app.route('/add_favorite_author/<int:book_id>', methods = ['POST'])
def add_favorite_author(book_id):
    books_model.Book.add_favorite_author(request.form)

    return redirect(f'/books/{book_id}')