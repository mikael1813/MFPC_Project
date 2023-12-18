class BookReview:
    def __init__(self, user_id, book_id, review_text, rating, review_id=-1, review_date=None):
        self.review_id = review_id
        self.user_id = user_id
        self.rating = rating
        self.book_id = book_id
        self.review_text = review_text
        self.review_date = review_date
