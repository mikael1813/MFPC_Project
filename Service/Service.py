from Repository.BookDatabase import BookDatabase
from Repository.UserDatabase import UserDatabase


class Service:
    def __init__(self):
        self.book_db = BookDatabase()
        self.user_db = UserDatabase()
        self.list_of_transactions = []
        self.list_of_locks = []
        self.list_of
