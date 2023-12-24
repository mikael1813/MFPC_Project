import json


class Author:
    def __init__(self, name, author_id=-1):
        self.name = name
        self.author_id = author_id

    def __dict__(self):
        # return dictionary of author object
        return {
            'author_id': self.author_id,
            'name': self.name
        }

    def __str__(self):
        # return json string of author object
        return json.dumps(self.__dict__())
