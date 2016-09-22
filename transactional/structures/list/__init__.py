__author__ = 'jgevirtz'

from ...core import History
from .actions import *

class List(object):
    def __init__(self, iterable=None):
        iterable = iterable if iterable else []
        self.list = list(iterable)

    def append(self, item):
        History.push_action(ListAppendAction(self.list, item))
        self.list.append(item)

    def pop(self):
        History.push_action(ListPopAction(self.list))
        return self.list.pop()

    def __iter__(self):
        for i in self.list:
            yield i

    def __add__(self, other):
        return List(self.list + other.list)

    def __getitem__(self, item):
        return self.list.__getitem__(item)

    def __str__(self):
        return "List({})".format(",".join(str(i) for i in self.list))

    def __len__(self):
        return len(self.list)

    def __eq__(self, other):
        return self.list == other.list
