__author__ = 'jgevirtz'

from ...core import Action

class DictSetAction(Action):
    def __init__(self, dict_, key, value):
        self.has_previous = key in dict_
        if self.has_previous:
            self.previous = dict_[key]

        self.dict = dict_
        self.key = key
        self.new_value = value

    def do(self):
        self.dict[self.key] = self.new_value

    def undo(self):
        if self.has_previous:
            self.dict[self.key] = self.previous
        else:
            del self.dict[self.key]


class DictRemoveAction(Action):
    def __init__(self, dict_, key):
        self.dict = dict_
        self.key = key
        self.previous = dict_[key]

    def do(self):
        del self.dict[self.key]

    def undo(self):
        self.dict[self.key] = self.previous






