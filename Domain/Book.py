class Book:
    def __init__(self, title, author_id, isbn, publish_year, genre, total_copies, book_id=-1):
        self.book_id = book_id
        self.title = title
        self.author_id = author_id
        self.isbn = isbn
        self.publish_year = publish_year
        self.genre = genre
        self.total_copies = total_copies
