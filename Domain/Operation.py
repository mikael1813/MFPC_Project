from enum import Enum
from Domain.Lock import LockType


class Record(Enum):
    AUTHOR = 1
    BOOK = 2
    BOOK_REVIEW = 3
    USER = 4
    USER_BORROWED_BOOK = 5
    USER_FINE = 6


class Table(Enum):
    USER = 1
    BOOK = 2


class OperationType(Enum):
    ADD = 1
    UPDATE = 2
    DELETE = 3
    SELECT = 4


class Operation:
    def __init__(self, table, record, operation_type, object=None, prev_object=None):
        self.table = table
        self.record = record
        self.operation_type = operation_type

        self.lock_type = LockType.WRITE
        if self.operation_type == OperationType.SELECT:
            self.lock_type = LockType.READ

        self.object = object
        self.prev_object = prev_object

    def get_inverse_operation(self):
        if self.operation_type == OperationType.ADD:
            inverse_operation_type = OperationType.DELETE
        elif self.operation_type == OperationType.UPDATE:
            inverse_operation_type = OperationType.UPDATE
        elif self.operation_type == OperationType.DELETE:
            inverse_operation_type = OperationType.ADD
        else:
            inverse_operation_type = None
        inverse_operation = Operation(self.table, self.record, inverse_operation_type, object=self.object,
                                      prev_object=self.prev_object)
        return inverse_operation
