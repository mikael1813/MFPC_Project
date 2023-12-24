import json


class BookReview:
    def __init__(self, user_id, book_id, review_text, rating, review_id=-1, review_date=None):
        self.review_id = review_id
        self.user_id = user_id
        self.rating = rating
        self.book_id = book_id
        self.review_text = review_text
        self.review_date = review_date

    def __dict__(self):
        # return dictionary of author object
        return {
            'review_id': self.review_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'book_id': self.book_id,
            'review_text': self.review_text,
            'review_date': self.review_date
        }

    def __str__(self):
        # return json string of book review object
        return json.dumps(self.__dict__())
