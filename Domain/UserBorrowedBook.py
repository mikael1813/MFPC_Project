class UserBorrowedBook:
    def __init__(self, user_id, book_id, borrow_date=None, due_date=None, return_date=None, record_id=-1):
        self.record_id = record_id
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date
