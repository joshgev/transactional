__author__ = 'jgevirtz'
from ...core import Action


class SetAddAction(Action):
    def __init__(self, set_, item):
        self.set = set_
        self.item = item
        self.null = item in set_

    def do(self):
        if not self.null:
            self.set.add(self.item)

    def undo(self):
        if not self.null:
            self.set.remove(self.item)


class SetBulkAddAction(Action):
    def __init__(self, set_, items):
        self.set = set
        self.new = items - set_

    def do(self):
        self.set |= self.new

    def undo(self):
        self.set -= self.new


class SetRemoveAction(Action):
    def __init__(self, set_, item):
        self.set = set_
        self.item = item

    def do(self):
        self.set.remove(self.item)

    def undo(self):
        self.set.add(self.item)


