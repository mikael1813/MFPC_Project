import json


class Book:
    def __init__(self, title, author_id, isbn, publish_year, genre, total_copies, book_id=-1):
        self.book_id = int(book_id)
        self.title = title
        self.author_id = author_id
        self.isbn = isbn
        self.publish_year = publish_year
        self.genre = genre
        self.total_copies = total_copies

    def __dict__(self):
        # return dictionary of author object
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author_id': self.author_id,
            'isbn': self.isbn,
            'publish_year': self.publish_year,
            'genre': self.genre,
            'total_copies': self.total_copies
        }

    def __str__(self):
        # return json string of book object
        return json.dumps(self.__dict__())
