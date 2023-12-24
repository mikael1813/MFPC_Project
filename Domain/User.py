import json


class User:
    def __init__(self, username, password, full_name, email, phone, user_id=-1):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.phone = phone

    def __dict__(self):
        # return dictionary of author object
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone
        }

    def __str__(self):
        # return json string of user object
        x = self.__dict__()
        x = json.dumps(x)
        return json.dumps(self.__dict__())
