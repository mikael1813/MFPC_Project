from enum import Enum


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


class LockType(Enum):
    READ = 1
    WRITE = 2
