class User:
    def __init__(self, username, password, full_name, email, phone, user_id=-1):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.phone = phone
