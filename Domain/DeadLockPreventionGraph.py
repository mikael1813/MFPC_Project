from Domain.Transaction import Transaction


class DeadLockPreventionGraph:
    # def __init__(self, lock_type: LockType, lock_table: Table, lock_record: Record, has_lock=False, wait_lock=False):
    #     self.lock_type = lock_type
    #     self.lock_table = lock_table
    #     self.lock_record = lock_record
    #     self.has_lock = has_lock
    #     self.wait_lock = wait_lock

    def __init__(self):
        self.adjacency_dict = {}

    def add_node(self, transaction: Transaction, wait_for_transaction: Transaction = None):
        if wait_for_transaction is None:
            self.adjacency_dict[transaction.transaction_id] = []
        else:
            if transaction.transaction_id not in self.adjacency_dict.keys():
                self.adjacency_dict[transaction.transaction_id] = [wait_for_transaction.transaction_id]
            else:
                self.adjacency_dict[transaction.transaction_id].append(wait_for_transaction.transaction_id)
            if wait_for_transaction.transaction_id not in self.adjacency_dict.keys():
                self.adjacency_dict[wait_for_transaction.transaction_id] = []

    def is_cyclic(self, transaction: Transaction = None):
        visited = set()
        stack = set()

        def is_cyclic_helper(vertex):
            visited.add(vertex)
            stack.add(vertex)
            for neighbor in self.adjacency_dict[vertex]:
                # neighbor = self.adjacency_dict[vertex]
                if neighbor is not None and neighbor not in visited:
                    output_list = is_cyclic_helper(neighbor)
                    if output_list is not False:
                        output_list.append(neighbor)
                        return output_list
                elif neighbor in stack:
                    return []
            stack.remove(vertex)
            return False

        # for vertex in self.adjacency_dict:
        vertex = transaction.transaction_id
        if vertex is not None:
            if vertex not in visited:
                output = is_cyclic_helper(vertex)
                if output is not False:
                    output.append(vertex)
                if output:
                    return output
        return False


if __name__ == '__main__':
    t1 = Transaction(1, 0, 0, 0)
    t2 = Transaction(2, 0, 0, 0)
    t3 = Transaction(3, 0, 0, 0)
    t4 = Transaction(4, 0, 0, 0)
    t5 = Transaction(5, 0, 0, 0)
    t6 = Transaction(6, 0, 0, 0)
    graph = DeadLockPreventionGraph()
    graph.add_node(t1, t2)
    graph.add_node(t1, t3)
    graph.add_node(t2, t3)
    graph.add_node(t3, t4)
    graph.add_node(t4, t1)
    graph.add_node(t5, t6)
    graph.add_node(t6, t5)
    xx = graph.is_cyclic(t5)
    print(xx)
    x = 0
