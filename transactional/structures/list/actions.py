__author__ = 'jgevirtz'

from ...core import Action

class ListAppendAction(Action):
    def __init__(self, list_, item):
        self.list = list_
        self.item = item

    def do(self):
        self.list.append(self.item)

    def undo(self):
        self.list.pop()

class ListPopAction(Action):
    def __init__(self, list_):
        self.list = list_
        self.item = list_[-1]

    def do(self):
        self.list.pop()

    def undo(self):
        self.list.append(self.item)





