from Domain.Enums import Record, Table, LockType
from Domain.Transaction import Transaction


class Lock:
    def __init__(self, lock_id: int, lock_type: LockType, record: Record, table: Table, transaction: Transaction):
        self.lock_id = lock_id
        self.lock_type = lock_type
        self.record = record
        self.table = table
        self.transaction = transaction


