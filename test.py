from Domain.Author import Author
from Domain.Book import Book
from Domain.User import User
from Repository.BookDatabase import BookDatabase
from Repository.UserDatabase import UserDatabase


def testing():
    book_db = BookDatabase()
    user_db = UserDatabase()

    # user_db.add_user(User('user1', 'pass1', 'Ana Maria', 'ssss@gmail.com'))
    # user_db.add_user_borrowed_book(UserBorrowedBook(1, 1, due_date='2023-12-15 10:05:23'))

    user = User('user1', 'pass1', 'Ana Maria', 'ssss@gmail.com', user_id=1)
    book = Book(1, 1, 1, 1, 1, 1, book_id=1)
    author = Author('Ion Caragiale', author_id=1)

    # user_db.add_user(user)
    # book_db.add_book(book)
    # user_db.add_user_borrowed_book(UserBorrowedBook(1, 1, due_date='2023-12-15 10:05:23'))
    # book_db.add_author(author)

    # th1 = Thread(target=service.dummy_transaction1)
    # th2 = Thread(target=service.dummy_transaction2)
    # th1.start()
    # th2.start()
    #
    # th1.join()
    # th2.join()

    # service.dummy_transaction2()
    # service.return_book(user.user_id, book.book_id)
    for user in user_db.get_users():
        print(user)
    for book in book_db.get_books():
        print(book)
    for review in user_db.get_user_borrows_book():
        print(review)
    for user_fine in user_db.get_users_fines():
        print(user_fine)
    for author in book_db.get_authors():
        print(author)


testing()
