import json

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
        inverse_operation = Operation(self.table, self.record, None, object=self.object,
                                      prev_object=self.prev_object)
        if self.operation_type == OperationType.ADD:
            inverse_operation.operation_type = OperationType.DELETE
        elif self.operation_type == OperationType.UPDATE:
            inverse_operation.operation_type = OperationType.UPDATE
            aux = self.object
            inverse_operation.object = self.prev_object
            inverse_operation.prev_object = aux
        elif self.operation_type == OperationType.DELETE:
            inverse_operation.operation_type = OperationType.ADD

        return inverse_operation

    def __dict__(self):
        return {
            'table': self.table,
            'record': self.record,
            'operation_type': self.operation_type.name,
            'object': self.object.__dict__(),
            'prev_object': self.prev_object.__dict__()
        }

    def __str__(self):
        return json.dumps(self.__dict__())
