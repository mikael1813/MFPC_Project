import threading

from Domain.Author import Author
from Repository.BookDatabase import BookDatabase
from Repository.UserDatabase import UserDatabase
from Domain.User import User
from Domain.Book import Book
from Domain.UserBorrowedBook import UserBorrowedBook
from Service.Service import Service

import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread

app = Flask(__name__)
CORS(app)
service = Service()


@app.route('/return_book', methods=['POST'])
def return_book():
    user_id = int((request.json['user_id']))
    book_id = int((request.json['book_id']))

    # try:
    service.return_book(user_id, book_id)
    # except Exception as e:
    #     print(e)
    #     return jsonify({'message': 'Some error occured'}), 400

    return jsonify({'message': 'Book returned successfully'}), 200


@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    user_id = int(request.json['user_id'])
    book_id = int(request.json['book_id'])
    number_of_days = None
    if 'number_of_days' in request.json:
        number_of_days = request.json['number_of_days']

    try:
        if number_of_days is None:
            service.borrow_book(user_id, book_id)
        else:
            service.borrow_book(user_id, book_id, number_of_days=number_of_days)
    except:
        return jsonify({'message': 'Book already borrowed'}), 400

    return jsonify({'message': 'Book borrowed successfully'}), 200


@app.route('/add_new_book_and_author', methods=['POST'])
def add_new_book_and_author():
    new_book = request.json['new_book']

    new_book = Book(new_book['title'], new_book['author_id'], new_book['isbn'], new_book['public_year'],
                    new_book['genre'],
                    new_book['total_copies'], book_id=new_book['book_id'])

    new_author = request.json['new_author']

    new_author = Author(new_author['author_name'], author_id=new_author['author_id'])

    service.add_new_book_and_author(new_book, new_author)


@app.route('/get_books_by_author', methods=['POST'])
def get_books_by_author():
    author_id = int(request.json['author_id'])

    if int(author_id) < 0:
        books = service.get_books_by_author()
    else:
        books = service.get_books_by_author(int(author_id))

    return jsonify({'books': [book.__dict__() for book in books]})


@app.route('/get_borrowed_books_by_user', methods=['POST'])
def get_borrowed_books_by_user():
    user_id = int(request.json['user_id'])

    books = service.get_borrowed_books_by_user(user_id)

    return jsonify({'books': [book.__dict__() for book in books]})


@app.route('/user', methods=['PUT'])
def update_user():
    new_user = request.json['user']

    new_user = User(new_user['username'], new_user['password'], new_user['full_name'], new_user['email'],
                    registration_date=None, user_id=new_user['user_id'])

    try:
        service.update_user(new_user)
    except:
        return jsonify('Email already used'), 400

    return jsonify({'message': 'User updated successfully'}), 200


@app.route('/user', methods=['POST'])
def add_user():
    new_user = request.json['user']

    new_user = User(new_user['username'], new_user['password'], new_user['full_name'], new_user['email'],
                    registration_date=None)

    try:
        service.add_user(new_user)
    except Exception as e:
        return jsonify('Email already used'), 400

    return jsonify({'message': 'User added successfully'}), 201


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/login', methods=['POST'])
def login():
    print(threading.current_thread().name)
    username = request.json['username']
    password = request.json['password']

    login_output = service.login(username, password)

    if not login_output:
        return jsonify({'message': 'Wrong credentials'}), 401
    else:
        return jsonify({'user_id': str(login_output)}), 200


def testing():
    book_db = BookDatabase()
    user_db = UserDatabase()

    # user_db.add_user(User('user1', 'pass1', 'Ana Maria', 'ssss@gmail.com', '0744444444'))
    # user_db.add_user_borrowed_book(UserBorrowedBook(1, 1, due_date='2023-12-15 10:05:23'))

    user = User('user1', 'pass1', 'Ana Maria', 'ssss@gmail.com', '0744444444', user_id=1)
    book = Book(1, 1, 1, 1, 1, 1, book_id=1)

    # user_db.add_user(user)
    # book_db.add_book(book)
    # user_db.add_user_borrowed_book(UserBorrowedBook(1, 1, due_date='2023-12-15 10:05:23'))

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


if __name__ == '__main__':
    app.run(debug=True)

    # service.add_user(User("kelu", "pass", "Kelu", "mail", "phone"))

    # testing()
