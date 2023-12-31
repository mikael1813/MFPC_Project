import json
from enum import Enum

from Domain.Operation import Operation


class Status(Enum):
    ACTIVE = 1
    ABORT = 2
    COMMIT = 3


class Transaction:
    def __init__(self, transaction_id: int, timestamp, status: Status, list_of_operations: [Operation]):
        self.transaction_id = transaction_id
        self.timestamp = timestamp
        self.status = status
        self.list_of_operations = list_of_operations
        self.data_dict = {}

    def __dict__(self):
        return {
            'transaction_id': self.transaction_id,
            'timestamp': self.timestamp,
            'status': self.status.name,
            'list_of_operations': [operation.__dict__() for operation in self.list_of_operations]
        }

    def __str__(self):
        # return json string of object
        return json.dumps(self.__dict__())

