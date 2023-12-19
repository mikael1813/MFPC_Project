from enum import Enum
from Transaction import Transaction


class Type(Enum):
    READ = 1
    WRITE = 2


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


class Lock:
    def __init__(self, lock_id: int, type: Type, record: Record, table: Table, transaction: Transaction):
        self.lock_id = lock_id
        self.type = type
        self.record = record
        self.table = table
        self.transaction = transaction
