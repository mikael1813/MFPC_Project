from enum import Enum

from Domain.Operation import Record, Table
from Transaction import Transaction


class LockType(Enum):
    READ = 1
    WRITE = 2


class Lock:
    def __init__(self, lock_id: int, type: LockType, record: Record, table: Table, transaction: Transaction):
        self.lock_id = lock_id
        self.type = type
        self.record = record
        self.table = table
        self.transaction = transaction
