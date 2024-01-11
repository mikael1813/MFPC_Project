import json


class UserBorrowedBook:
    def __init__(self, user_id, book_id, borrow_date=None, due_date=None, return_date=None, record_id=-1):
        self.record_id = int(record_id)
        self.user_id = int(user_id)
        self.book_id = int(book_id)
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date

    def __dict__(self):
        # return dictionary of author object
        return {
            'record_id': self.record_id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'borrow_date': self.borrow_date,
            'due_date': self.due_date,
            'return_date': self.return_date
        }
    def __str__(self):
        # return json string of user borrowed book object
        return json.dumps(self.__dict__())
