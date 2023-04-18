from books_app.config.mysqlconnection import connectToMySQL

from books_app.models import authors_model

from books_app import DATABASE

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.author_favs = []

    # Create book
    @classmethod 
    def create(cls, data):
        query = """
            INSERT INTO books(title, num_of_pages) 
            VALUES(%(title)s, %(num_of_pages)s);
        """

        return connectToMySQL(DATABASE).query_db(query, data)
    
    # Get all books
    @classmethod 
    def get_all_books(cls):
        query = """
            SELECT * FROM books;
        """

        results = connectToMySQL(DATABASE).query_db(query)

        books = []
        if results:
            for row in results:
                new_book = cls(row)
                books.append(new_book)
        else:
            return False 
        
        return books

    # Get book with favorites
    @classmethod 
    def get_book_favorites(cls, id):
        data = {
            'id' : id
        }

        query = """
            SELECT * FROM books 
            LEFT JOIN favorites ON books.id = favorites.book_id 
            LEFT JOIN authors ON authors.id = favorites.author_id 
            WHERE books.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        book = cls(results[0])

        for row in results:
            author_data = {
                **row,
                'id' : row['authors.id'],
                'created_at' : row['authors.created_at'],
                'updated_at' : row['authors.updated_at']
            }

            book.author_favs.append(authors_model.Author(author_data))
        
        return book

    # Add favorite author
    @classmethod 
    def add_favorite_author(cls, data):
        query = """
            INSERT INTO favorites(book_id, author_id) 
            VALUES(%(book_id)s, %(author_id)s);
        """

        connectToMySQL(DATABASE).query_db(query, data)