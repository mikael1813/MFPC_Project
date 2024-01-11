import json


class User:
    def __init__(self, username, password, full_name, email, registration_date=None, user_id=-1):
        self.user_id = int(user_id)
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.registration_date = registration_date

    def __dict__(self):
        # return dictionary of author object
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'full_name': self.full_name,
            'email': self.email,
            'registration_date': self.registration_date
        }

    def __str__(self):
        # return json string of user object
        x = self.__dict__()
        x = json.dumps(x)
        return json.dumps(self.__dict__())
