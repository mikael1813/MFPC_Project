import json


class UserFine:
    def __init__(self, user_id, fine_amount, fine_description, payment_status=False, fine_id=-1):
        self.fine_id = fine_id
        self.user_id = user_id
        self.fine_amount = fine_amount
        self.fine_description = fine_description
        self.fine_description = fine_description
        self.payment_status = payment_status

    def __dict__(self):
        # return dictionary of author object
        return {
            'fine_id': self.fine_id,
            'user_id': self.user_id,
            'fine_amount': self.fine_amount,
            'fine_description': self.fine_description,
            'payment_status': self.payment_status
        }

    def __str__(self):
        # return json string of user fine object
        return json.dumps(self.__dict__())
