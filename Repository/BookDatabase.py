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
        cursor.execute('''CREATE TABLE IF NOT EXISTS book
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
        cursor.execute('''CREATE TABLE IF NOT EXISTS book_review
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
        cursor.execute('''CREATE TABLE IF NOT EXISTS author
                            (author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            author_name TEXT NOT NULL
                            );''')
        self.connection.commit()

    def add_book(self, book: Book):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO book (title, author_id, isbn, publish_year, genre, total_copies, "
                       "available_copies) VALUES (?, ?, ?, ?, ?, ?, ?);",
                       (book.title, book.author_id, book.isbn, book.publish_year, book.genre, book.total_copies))
        self.connection.commit()
        cursor.close()

    def add_book_review(self, book_review: BookReview):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO book_review (user_id, book_id, review_text, rating) VALUES (?, ?, ?, ?);",
                       (book_review.user_id, book_review.book_id, book_review.review_text, book_review.rating))
        self.connection.commit()
        cursor.close()

    def add_author(self, author: Author):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO author (author_name) VALUES (?);",
                       (author.name,))
        self.connection.commit()
        cursor.close()
