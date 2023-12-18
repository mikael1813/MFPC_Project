import sqlite3
from Domain.User import User
from Domain.UserBorrowedBook import UserBorrowedBook
from Domain.UserFine import UserFine


class UserDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('user.db')
        self.init_user_table()
        self.init_user_borrowed_book_table()
        self.init_user_fines_table()

    def init_user_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()
        cursor.close()

    def init_user_borrowed_book_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_borrowed_book (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                return_date TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )""")
        self.connection.commit()
        cursor.close()

    def init_user_fines_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_fines (
                fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                fine_amount REAL NOT NULL,
                fine_description TEXT NOT NULL,
                payment_status BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )""")
        self.connection.commit()
        cursor.close()

    def add_user(self, user: User):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO users (username, password, full_name, email) VALUES (?, ?, ?, ?);",
                       (user.username, user.password, user.full_name, user.email))
        self.connection.commit()
        cursor.close()

    def get_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users;")
        result = cursor.fetchall()
        cursor.close()
        return result

    def add_user_borrowed_book(self, user_borrowed_book: UserBorrowedBook):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO user_borrowed_book (user_id, book_id, return_date) VALUES (?, ?, ?);",
                       (user_borrowed_book.user_id, user_borrowed_book.book_id, user_borrowed_book.return_date))
        self.connection.commit()
        cursor.close()

    def add_user_fine(self, user_fine: UserFine):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO user_fines (user_id, fine_amount, fine_description) VALUES (?, ?, ?);",
                       (user_fine.user_id, user_fine.fine_amount, user_fine.fine_description))
        self.connection.commit()
        cursor.close()
