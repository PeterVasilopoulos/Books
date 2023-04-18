from flask import render_template, request, redirect

from books_app.models import authors_model, books_model

from books_app import app

# Default redirects to authors page
@app.route('/')
def default():
    return redirect('/authors')

# Authors page
@app.route('/authors')
def authors():
    all_authors = authors_model.Author.get_all_authors()

    if all_authors:
        return render_template('authors.html', authors = all_authors)
    else:
        return render_template('authors.html')

# Create new author
@app.route('/create_author', methods = ['POST'])
def create_author():
    authors_model.Author.create(request.form)

    return redirect('/authors')

# View author's favorites
@app.route('/authors/<int:id>')
def authors_favorites(id):
    results = authors_model.Author.get_author_favorites(id)

    books = books_model.Book.get_all_books()

    if results and books:
        return render_template('authors_favorites.html', results = results, books = books)
    else:
        return redirect('/')

# Add favorite book
@app.route('/add_favorite_book/<int:author_id>', methods = ['POST'])
def add_favorite_book(author_id):
    authors_model.Author.add_favorite_book(request.form)

    return redirect(f'/authors/{author_id}')