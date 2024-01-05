from Repository.BookDatabase import BookDatabase
from Repository.UserDatabase import UserDatabase
from Domain.User import User
from Domain.Book import Book
from Domain.UserBorrowedBook import UserBorrowedBook
from Service.Service import Service

from threading import Thread

if __name__ == '__main__':
    book_db = BookDatabase()
    user_db = UserDatabase()

    # user_db.add_user(User('user1', 'pass1', 'Ana Maria', 'ssss@gmail.com', '0744444444'))
    # user_db.add_user_borrowed_book(UserBorrowedBook(1, 1, due_date='2023-12-15 10:05:23'))

    user = User('user1', 'pass1', 'Ana Maria', 'ssss@gmail.com', '0744444444', user_id=1)
    book = Book(1, 1, 1, 1, 1, 1, book_id=1)

    # user_db.add_user(user)
    # book_db.add_book(book)
    # user_db.add_user_borrowed_book(UserBorrowedBook(1, 1, due_date='2023-12-15 10:05:23'))

    service = Service()
    th1 = Thread(target=service.dummy_transaction1)
    th2 = Thread(target=service.dummy_transaction2)
    # th1.start()
    # th2.start()
    #
    # th1.join()
    # th2.join()
    # service.return_book(user.user_id, book.book_id)
    for user in user_db.get_users():
        print(user)
    for book in book_db.get_books():
        print(book)
    for review in user_db.get_user_borrows_book():
        print(review)
    for user_fine in user_db.get_users_fines():
        print(user_fine)
