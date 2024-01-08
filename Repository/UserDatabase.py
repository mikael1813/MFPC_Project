import sqlite3
from Domain.User import User
from Domain.UserBorrowedBook import UserBorrowedBook
from Domain.UserFine import UserFine


class UserDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('user.db', check_same_thread=False)
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
                due_date TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, '+30 days')),
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

    def update_user(self, user: User):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET username = ?, password = ?, full_name = ?, email = ? WHERE user_id = ?;",
                       (user.username, user.password, user.full_name, user.email, user.user_id))
        self.connection.commit()
        cursor.close()

    def get_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users;")
        result = cursor.fetchall()
        cursor.close()
        output_list = []
        for user_tuple in result:
            user = User(user_tuple[1], user_tuple[2], user_tuple[3], user_tuple[4], user_tuple[5],
                        user_id=user_tuple[0])
            output_list.append(user)
        return output_list

    def get_user_by_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,))
        result = cursor.fetchall()
        cursor.close()
        user = User(result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], user_id=result[0][0])
        return user

    def add_user_borrowed_book(self, user_borrowed_book: UserBorrowedBook):
        cursor = self.connection.cursor()

        query_values = "(user_id, book_id"
        query_data = "(?, ?"
        parameters = (user_borrowed_book.user_id, user_borrowed_book.book_id)

        if user_borrowed_book.borrow_date is not None:
            query_values += ", borrow_date"
            query_data += ", ?"
            parameters += (user_borrowed_book.borrow_date,)
        if user_borrowed_book.due_date is not None:
            query_values += ", due_date"
            query_data += ", ?"
            parameters += (user_borrowed_book.due_date,)
        if user_borrowed_book.return_date is not None:
            query_values += ", return_date"
            query_data += ", ?"
            parameters += (user_borrowed_book.return_date,)

        cursor.execute(f"INSERT INTO user_borrowed_book {query_values}) VALUES {query_data});", parameters)

        self.connection.commit()
        cursor.close()

    def update_user_borrowed_book(self, user_borrowed_book: UserBorrowedBook):
        cursor = self.connection.cursor()

        query_values = ""
        parameters = ()

        if user_borrowed_book.borrow_date is not None:
            query_values += "borrow_date = ?, "
            parameters += (user_borrowed_book.borrow_date,)
        if user_borrowed_book.due_date is not None:
            query_values += "due_date = ?, "
            parameters += (user_borrowed_book.due_date,)
        if user_borrowed_book.return_date is not None:
            query_values += "return_date = ?, "
            parameters += (user_borrowed_book.return_date,)

        query_values = query_values[:-2]
        parameters += (user_borrowed_book.user_id, user_borrowed_book.book_id)

        cursor.execute(f"UPDATE user_borrowed_book SET {query_values} WHERE user_id = ? AND book_id = ?;", parameters)

        self.connection.commit()
        cursor.close()

    def get_borrow_of_book(self, user_id, book_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM user_borrowed_book WHERE user_id = ? AND book_id = ?", (user_id, book_id))
        result = cursor.fetchall()
        cursor.close()
        borrow_of_book = UserBorrowedBook(result[0][1], result[0][2], borrow_date=result[0][3], due_date=result[0][4],
                                          return_date=result[0][5], record_id=result[0][0])
        return borrow_of_book

    def get_user_borrows_book(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM user_borrowed_book;")
        result = cursor.fetchall()
        cursor.close()
        output_list = []
        for user_borrow_tuple in result:
            user_borrow = UserBorrowedBook(user_borrow_tuple[1], user_borrow_tuple[2], borrow_date=user_borrow_tuple[3],
                                           due_date=user_borrow_tuple[4], return_date=user_borrow_tuple[5],
                                           record_id=user_borrow_tuple[0])
            output_list.append(user_borrow)
        return output_list

    def add_user_fine(self, user_fine: UserFine):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO user_fines (user_id, fine_amount, fine_description) VALUES (?, ?, ?);",
                       (user_fine.user_id, user_fine.fine_amount, user_fine.fine_description))
        self.connection.commit()
        cursor.close()

    def get_users_fines(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM user_fines;")
        result = cursor.fetchall()
        cursor.close()
        output_list = []
        for user_fine_tuple in result:
            user_fine = UserFine(user_fine_tuple[1], user_fine_tuple[2], user_fine_tuple[3], user_fine_tuple[4],
                                 fine_id=user_fine_tuple[0])
            output_list.append(user_fine)
        return output_list
