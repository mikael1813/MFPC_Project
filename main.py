from Repository.BookDatabase import BookDatabase
from Repository.UserDatabase import UserDatabase
from Domain.User import User

if __name__ == '__main__':
    book_db = BookDatabase()
    user_db = UserDatabase()

    # user_db.add_user(User('user1', 'pass1', 'Ana Maria', 'ssss@gmail.com', '0744444444'))
    print(user_db.get_users())
