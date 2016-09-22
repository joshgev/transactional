__author__ = 'jgevirtz'

class Action(object):
    def do(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError


class Transaction(object):
    def __init__(self, name=None):
        self.actions = []
        self.parent_transaction = History.current_transaction
        self.name = name

    def push_action(self, action):
        self.actions.append(action)

    def do(self):
        History.do_transaction(self)

    def undo(self):
        History.undo_transaction(self)

    def roll_back(self):
        History.roll_back(self)
        return History.current_transaction

    def roll_forward(self):
        History.roll_forward(self)
        return History.current_transaction

    def ancestry(self, stop=None):
        current = self
        while current is not stop:
            yield current
            current = current.parent_transaction

    def __enter__(self):
        History.active_transaction = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        History.active_transaction = None
        History.current_transaction = self
        History.applied_transactions.add(self)


class BaseTransaction(object):
    instance = None

    def __init__(self):
        if self.instance:
            assert False
        self.instance = self

    def push_action(self, action):
        assert False

    def do(self):
        assert False

    def undo(self):
        assert False

    def ancestry(self, stop=None):
        assert False


class History(object):
    # The most recently applied transaction
    current_transaction = BaseTransaction()

    # Transaction currently being written to
    active_transaction = None

    applied_transactions = set()

    @staticmethod
    def push_action(action):
        if History.active_transaction is not None:
            History.active_transaction.push_action(action)

    @staticmethod
    def do_transaction(transaction):
        assert History.current_transaction is transaction.parent_transaction
        for action in transaction.actions:
            action.do()
        History.applied_transactions.add(transaction)
        History.current_transaction = transaction

    @staticmethod
    def undo_transaction(transaction):
        assert History.current_transaction is transaction
        for action in reversed(transaction.actions):
            action.undo()
        History.applied_transactions.remove(transaction)
        History.current_transaction = transaction.parent_transaction

    @staticmethod
    def roll_forward(transaction):
        assert History.current_transaction in transaction.ancestry()
        transactions = reversed([t for t in transaction.ancestry(History.current_transaction)])
        for t in transactions:
            History.do_transaction(t)

    @staticmethod
    def roll_back(transaction):
        assert transaction in History.applied_transactions
        while History.current_transaction is not transaction:
            History.undo_transaction(History.current_transaction)

class SetAttributeAction(Action):
    def __init__(self, o, k, v):
        self.o = o
        self.k = k
        self.v = v

    def do(self):
        setattr(self.o, self.k, self.v)

    def undo(self):
        delattr(self.o, self.k)

class ResetAttributeAction(Action):
    def __init__(self, o, k, v):
        self.o = o
        self.k = k
        self.v = v
        self.p = getattr(o, k)

    def do(self):
        setattr(self.o, self.k, self.v)

    def undo(self):
        setattr(self.o, self.k, self.p)

def transactional(name=None):
    def decorator(func):
        def new_func(*args, **kwargs):
            with Transaction(name) as transaction:
                func(*args, **kwargs)
            return transaction
        return new_func
    return decorator


class UpdateVariableAction(Action):
    def __init__(self, variable, value):
        self.variable = variable
        self.previous_value = variable.value
        self.new_value = value

    def do(self):
        self.variable.value = self.new_value

    def undo(self):
        self.variable.value = self.previous_value


class Variable(object):
    def __init__(self, value=None):
        self.value = value

    def __call__(self, val=None):
        if not val:
            return self.value
        History.push_action(UpdateVariableAction(self, val))
        self.value = val

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.value)
