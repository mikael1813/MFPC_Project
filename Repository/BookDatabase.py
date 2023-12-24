import sqlite3

from Domain.Book import Book
from Domain.BookReview import BookReview
from Domain.Author import Author


class BookDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('book.db')
        self.init_book_table()
        self.init_book_review_table()
        self.init_author_table()

    def init_book_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books
                            (book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            author_id INTEGER NOT NULL,
                            isbn TEXT NOT NULL,
                            publish_year INTEGER NOT NULL,
                            genre TEXT NOT NULL,
                            total_copies INTEGER NOT NULL,
                            FOREIGN KEY (author_id) REFERENCES author(author_id)
                            );''')
        self.connection.commit()

    def init_book_review_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS book_reviews
                            (review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            book_id INTEGER NOT NULL,
                            review_text TEXT NOT NULL,
                            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                            review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (book_id) REFERENCES book(book_id)
                            );''')
        self.connection.commit()

    def init_author_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS authors
                            (author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            author_name TEXT NOT NULL
                            );''')
        self.connection.commit()

    def add_book(self, book: Book):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO books (title, author_id, isbn, publish_year, genre, total_copies"
                       ") VALUES (?, ?, ?, ?, ?, ?);",
                       (book.title, book.author_id, book.isbn, book.publish_year, book.genre, book.total_copies))
        self.connection.commit()
        cursor.close()

    def get_books(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books;")
        result = cursor.fetchall()
        cursor.close()
        output_list = []
        for book in result:
            output_list.append(Book(book[1], book[2], book[3], book[4], book[5], book[6], book_id=book[0]))
        return output_list

    def get_book_by_id(self, book_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id = ?;", (book_id,))
        result = cursor.fetchall()
        cursor.close()
        book = Book(result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6],
                    book_id=result[0][0])
        return book

    def add_book_review(self, book_review: BookReview):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO book_reviews (user_id, book_id, review_text, rating) VALUES (?, ?, ?, ?);",
                       (book_review.user_id, book_review.book_id, book_review.review_text, book_review.rating))
        self.connection.commit()
        cursor.close()

    def add_author(self, author: Author):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO authors (author_name) VALUES (?);",
                       (author.name,))
        self.connection.commit()
        cursor.close()
