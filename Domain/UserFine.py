class UserFine:
    def __init__(self, user_id, fine_amount, fine_description, payment_status=False, fine_id=-1):
        self.fine_id = fine_id
        self.user_id = user_id
        self.fine_amount = fine_amount
        self.fine_description = fine_description
        self.fine_description = fine_description
        self.payment_status = payment_status
