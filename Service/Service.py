import threading
import time
from datetime import datetime, timedelta
from threading import Lock

from Domain.Author import Author
from Domain.Book import Book
from Domain.CustomLock import CustomLock
from Domain.DeadLockPreventionGraph import DeadLockPreventionGraph
from Domain.Enums import Record, Table, OperationType, LockType
from Domain.Operation import Operation
from Domain.Transaction import Transaction, Status
from Domain.User import User
from Domain.UserBorrowedBook import UserBorrowedBook
from Domain.UserFine import UserFine
from Domain.constants import users, user, books, book, borrowed_book, returned_book
from Repository.BookDatabase import BookDatabase
from Repository.UserDatabase import UserDatabase

mutex = Lock()


class Service:
    def __init__(self):
        self.book_db = BookDatabase()
        self.user_db = UserDatabase()
        # t1 = Transaction(1, 0, Status.ACTIVE, [])
        # self.list_of_transactions = [t1]
        # self.list_of_locks = [
        #     CustomLock(1, LockType.READ, Record.BOOK, Table.BOOK, t1)]
        self.list_of_transactions = []
        self.list_of_locks = []
        self.graph_for_deadlock_prevention = DeadLockPreventionGraph()
        self.fine_rate = 10  # USD per day

    # def return_book(self, user: User, book: Book):
    #     borrow = self.user_db.get_borrow_of_book(user.user_id, book.book_id)
    #     return_date = datetime.strptime(borrow[0][4], '%Y-%m-%d %H:%M:%S')
    #     current_time = datetime.now()
    #
    #     if current_time > return_date:
    #         days = (current_time - return_date).days + 1
    #         fine = days * self.fine_rate
    #         self.user_db.add_user_fine(UserFine(user.user_id, fine, "Late " + str(days) + " days.", fine_id=1))

    def can_acquire_lock(self, operation: Operation):
        for lock in self.list_of_locks:
            if lock.record == operation.record and (
                    lock.lock_type == LockType.WRITE or operation.lock_type == LockType.WRITE):
                return False
        return True

    def get_blocking_transactions(self, operation: Operation):
        list_of_blocking_transactions = []
        for lock in self.list_of_locks:
            if lock.record == operation.record and (
                    lock.lock_type == LockType.WRITE or operation.lock_type == LockType.WRITE):
                list_of_blocking_transactions.append(lock.transaction)
        return list_of_blocking_transactions

    def check_number_of_read_locks(self, record: Record):
        number_of_read_locks = 0
        for lock in self.list_of_locks:
            if lock.record == record:
                if lock.lock_type == LockType.WRITE:
                    return False
                else:
                    number_of_read_locks += 1
        if number_of_read_locks > 1:
            return False
        return True

    def can_upgrade_lock(self, operation: Operation, transaction: Transaction):
        for lock in self.list_of_locks:
            if (lock.record == operation.record and lock.transaction == transaction and
                    self.check_number_of_read_locks(operation.record)):
                lock.lock_type = LockType.WRITE
                return True

    def release_locks(self, transaction: Transaction):
        with mutex:
            locks_to_be_released = []
            for lock in self.list_of_locks:
                if lock.transaction == transaction:
                    locks_to_be_released.append(lock)

            for lock in locks_to_be_released:
                self.list_of_locks.remove(lock)

    def acquire_lock(self, operation: Operation, transaction: Transaction):
        lock_id = self.generate_lock_id()
        lock = CustomLock(lock_id, operation.lock_type, operation.record, operation.table, transaction)
        self.list_of_locks.append(lock)

    def has_lock(self, operation: Operation, transaction: Transaction):
        for lock in self.list_of_locks:
            if lock.transaction == transaction and lock.record == operation.record:
                if lock.lock_type == LockType.WRITE:
                    return True
                elif lock.lock_type == LockType.READ and operation.lock_type == LockType.READ:
                    return True
        return False

    def try_to_acquire_lock(self, operation: Operation, transaction: Transaction):
        with mutex:
            if self.has_lock(operation, transaction):
                return True
            elif self.can_acquire_lock(operation):
                self.acquire_lock(operation, transaction)

                return True
            elif self.can_upgrade_lock(operation, transaction):

                return True
        return False

    def begin_transaction(self, transaction: Transaction):
        successful_operations = []
        # reverse_transaction = Transaction(transaction.transaction_id, transaction.timestamp, transaction.status,
        #                                   [])
        for operation in transaction.list_of_operations:
            if operation.operation_type == OperationType.ADD:
                time.sleep(5)
            while True:
                print(threading.currentThread())
                # TODO reverse transaction for versioning
                if self.try_to_acquire_lock(operation, transaction):
                    self.start_operation(operation, transaction)
                    inverse_operation = operation.get_inverse_operation()
                    successful_operations.append(inverse_operation)
                    # reverse_transaction.list_of_operations.append(inverse_operation)
                    break
                else:
                    list_of_blocking_transactions = self.get_blocking_transactions(operation)
                    for blocking_transaction in list_of_blocking_transactions:
                        with mutex:
                            self.graph_for_deadlock_prevention.add_node(transaction, blocking_transaction)

                    with mutex:
                        cyclic_nodes = self.graph_for_deadlock_prevention.is_cyclic(transaction)
                        if type(cyclic_nodes) is list:
                            cyclic_nodes.sort()
                        if cyclic_nodes is not False and transaction.transaction_id == cyclic_nodes[-1]:
                            transaction.status = Status.ABORT
                            self.graph_for_deadlock_prevention.remove_node(transaction)
                            break
                    print(str(threading.currentThread()) + " can't acquire lock, waiting")
                    time.sleep(1)

        if transaction.status == Status.ABORT:
            for operation in reversed(successful_operations):
                self.start_operation(operation, transaction)
            self.release_locks(transaction)

            time.sleep(1)

            transaction.data_dict = {}
            transaction.status = Status.ACTIVE
            self.begin_transaction(transaction)
        else:
            transaction.status = Status.COMMIT
            self.release_locks(transaction)

    def return_book(self, user_id, book_id):
        transaction = Transaction(self.generate_transaction_id(), datetime.now(), Status.ACTIVE, [])
        with mutex:
            self.list_of_transactions.append(transaction)
        operation1 = Operation(Table.USER, Record.USER, OperationType.SELECT, object=user_id)
        operation2 = Operation(Table.BOOK, Record.BOOK, OperationType.SELECT, object=book_id)
        operation3 = Operation(Table.USER, Record.USER_BORROWED_BOOK, OperationType.SELECT, object=(user_id, book_id))
        operation4 = Operation(Table.USER, Record.USER_BORROWED_BOOK, OperationType.UPDATE,
                               object=UserBorrowedBook(user_id, book_id, return_date=datetime.now()),
                               prev_object=None)
        operation5 = Operation(Table.USER, Record.USER_FINE, OperationType.ADD)

        list_of_operations = [operation1, operation2, operation3, operation4, operation5]
        transaction.list_of_operations = list_of_operations
        self.begin_transaction(transaction)

    def borrow_book(self, user_id, book_id, number_of_days=30):
        transaction = Transaction(self.generate_transaction_id(), datetime.now(), Status.ACTIVE, [])
        with mutex:
            self.list_of_transactions.append(transaction)
        operation1 = Operation(Table.USER, Record.USER, OperationType.SELECT, object=user_id)
        operation2 = Operation(Table.BOOK, Record.BOOK, OperationType.SELECT, object=book_id)
        operation3 = Operation(Table.USER, Record.USER_BORROWED_BOOK, OperationType.ADD,
                               object=UserBorrowedBook(user_id, book_id, borrow_date=datetime.now(),
                                                       due_date=datetime.now() + timedelta(number_of_days)))
        list_of_operations = [operation1, operation2, operation3]
        transaction.list_of_operations = list_of_operations
        self.begin_transaction(transaction)

    def add_new_book_and_author(self, new_book: Book, new_author: Author):
        transaction = Transaction(self.generate_transaction_id(), datetime.now(), Status.ACTIVE, [])
        with mutex:
            self.list_of_transactions.append(transaction)
        operation1 = Operation(Table.BOOK, Record.BOOK, OperationType.ADD, object=new_book)
        if new_author is not None:
            operation2 = Operation(Table.BOOK, Record.AUTHOR, OperationType.ADD, object=new_author)
            transaction.list_of_operations = [operation1, operation2]
        else:
            transaction.list_of_operations = [operation1]
        self.begin_transaction(transaction)

    def get_books_by_author(self, author_id):
        transaction = Transaction(self.generate_transaction_id(), datetime.now(), Status.ACTIVE, [])
        with mutex:
            self.list_of_transactions.append(transaction)
        operation1 = Operation(Table.BOOK, Record.BOOK, OperationType.SELECT, object=author_id)
        list_of_operations = [operation1]
        transaction.list_of_operations = list_of_operations
        self.begin_transaction(transaction)

    def get_borrowed_books_by_user(self, user_id):
        transaction = Transaction(self.generate_transaction_id(), datetime.now(), Status.ACTIVE, [])
        with mutex:
            self.list_of_transactions.append(transaction)
        operation1 = Operation(Table.USER, Record.USER_BORROWED_BOOK, OperationType.SELECT, object=user_id)
        operation2 = Operation(Table.BOOK, Record.BOOK, OperationType.SELECT, object=None)
        list_of_operations = [operation1, operation2]
        transaction.list_of_operations = list_of_operations
        self.begin_transaction(transaction)

    def update_user(self, new_user: User):
        transaction = Transaction(self.generate_transaction_id(), datetime.now(), Status.ACTIVE, [])
        with mutex:
            self.list_of_transactions.append(transaction)
        operation1 = Operation(Table.USER, Record.USER, OperationType.UPDATE, object=new_user)
        list_of_operations = [operation1]
        transaction.list_of_operations = list_of_operations
        self.begin_transaction(transaction)

    def add_user(self, new_user: User):
        transaction = Transaction(self.generate_transaction_id(), datetime.now(), Status.ACTIVE, [])
        with mutex:
            self.list_of_transactions.append(transaction)
        operation1 = Operation(Table.USER, Record.USER, OperationType.ADD, object=new_user)
        list_of_operations = [operation1]
        transaction.list_of_operations = list_of_operations
        self.begin_transaction(transaction)

    def dummy_transaction1(self):
        transaction = Transaction(self.generate_transaction_id(), 0, Status.ACTIVE, [])
        with mutex:
            self.list_of_transactions.append(transaction)
        operation1 = Operation(Table.USER, Record.USER, OperationType.SELECT, object=1)
        operation2 = Operation(Table.BOOK, Record.BOOK, OperationType.ADD, object=Book(1, 1, 2, 2, 2, 2, book_id=99))
        list_of_operations = [operation1, operation2]
        transaction.list_of_operations = list_of_operations
        self.begin_transaction(transaction)

    def dummy_transaction2(self):
        transaction = Transaction(self.generate_transaction_id(), 0, Status.ACTIVE, [])
        with mutex:
            self.list_of_transactions.append(transaction)
        operation1 = Operation(Table.BOOK, Record.BOOK, OperationType.SELECT, object=1)
        operation2 = Operation(Table.USER, Record.USER, OperationType.ADD,
                               object=User('2', '2', 'Aku', 'aaaa@gmail.com', '0744444444', user_id=99))
        list_of_operations = [operation1, operation2]
        transaction.list_of_operations = list_of_operations
        self.begin_transaction(transaction)

    def start_operation(self, operation, transaction):
        if operation.record == Record.USER:
            if operation.operation_type == OperationType.SELECT:
                if operation.object is None:
                    transaction.data_dict[users] = self.get_all_users()
                else:
                    transaction.data_dict[user] = self.get_user(operation.object)
            elif operation.operation_type == OperationType.ADD:
                self.user_db.add_user(operation.object)
        elif operation.record == Record.BOOK:
            if operation.operation_type == OperationType.SELECT:
                if operation.object is None:
                    transaction.data_dict[books] = self.get_all_books()
                else:
                    transaction.data_dict[book] = self.get_book(operation.object)
            elif operation.operation_type == OperationType.ADD:
                self.book_db.add_book(operation.object)
        elif operation.record == Record.USER_BORROWED_BOOK:
            if operation.operation_type == OperationType.SELECT:
                if operation.object is None:
                    pass
                    # transaction.data_dict[borrowed_books] = self.get_all_users()
                else:
                    transaction.data_dict[borrowed_book] = self.get_borrowed_book(operation.object[0],
                                                                                  operation.object[1])
            elif operation.operation_type == OperationType.UPDATE:
                operation.prev_object = transaction.data_dict[borrowed_book]
                operation.object = transaction.data_dict[borrowed_book]
                operation.object.return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                transaction.data_dict[returned_book] = operation.object
                self.update_borrow_book(operation.object)

        elif operation.record == Record.USER_FINE:
            if operation.operation_type == OperationType.ADD:
                user_returned_book: UserBorrowedBook = transaction.data_dict[returned_book]
                self.check_for_user_fine(user_returned_book)

    def get_all_users(self):
        return self.user_db.get_users()

    def get_user(self, user_id):
        return self.user_db.get_user_by_id(user_id)

    def get_all_books(self):
        return self.book_db.get_books()

    def get_book(self, book_id):
        return self.book_db.get_book_by_id(book_id)

    def get_borrowed_book(self, user_id, book_id):
        return self.user_db.get_borrow_of_book(user_id, book_id)

    def update_borrow_book(self, user_borrowed_book: UserBorrowedBook):
        self.user_db.update_user_borrowed_book(user_borrowed_book)

    def generate_transaction_id(self):
        return len(self.list_of_transactions) + 1

    def generate_lock_id(self):
        return len(self.list_of_locks) + 1

    def check_for_user_fine(self, user_borrowed_book: UserBorrowedBook):
        return_date = datetime.strptime(user_borrowed_book.return_date, '%Y-%m-%d %H:%M:%S')
        due_date = datetime.strptime(user_borrowed_book.due_date, '%Y-%m-%d %H:%M:%S')

        if return_date > due_date:
            days = (return_date - due_date).days + 1
            fine = days * self.fine_rate
            self.user_db.add_user_fine(UserFine(user_borrowed_book.user_id, fine, "Late " + str(days) + " days."))
