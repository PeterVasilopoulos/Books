from books_app.config.mysqlconnection import connectToMySQL

from books_app.models import books_model

from books_app import DATABASE

class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.book_favs = []
    
    # Create author
    @classmethod 
    def create(cls, data):
        query = """
            INSERT INTO authors(name) 
            VALUES(%(name)s);
        """

        return connectToMySQL(DATABASE).query_db(query, data)
    
    # Get all authors
    @classmethod 
    def get_all_authors(cls):
        query = """
            SELECT * FROM authors;
        """

        results = connectToMySQL(DATABASE).query_db(query)

        authors = []
        if results:
            for row in results:
                new_author = cls(row)
                authors.append(new_author)
        else:
            return False

        return authors

    # Get author with favorites
    @classmethod 
    def get_author_favorites(cls, id):
        data = {
            'id' : id
        }

        query = """
            SELECT * FROM authors
            LEFT JOIN favorites ON authors.id = favorites.author_id 
            LEFT JOIN books ON books.id = favorites.book_id 
            WHERE authors.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        author = cls(results[0])

        for row in results:
            book_data = {
                **row,
                'id' : row['books.id'],
                'created_at' : row['books.created_at'],
                'updated_at' : row['books.updated_at']
            }

            author.book_favs.append(books_model.Book(book_data))
        
        return author

    # Add favorite book
    @classmethod 
    def add_favorite_book(cls, data):
        query = """
            INSERT INTO favorites(book_id, author_id) 
            VALUES(%(book_id)s, %(author_id)s);
        """

        connectToMySQL(DATABASE).query_db(query, data)