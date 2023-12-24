from Domain.Enums import OperationType, LockType


class Operation:
    def __init__(self, table, record, operation_type: OperationType, object=None, prev_object=None):
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
