__author__ = 'jgevirtz'

from .actions import *
from ...core import History
from collections import defaultdict

class Dict(object):
    def __init__(self, iterable=None, default=None):
        iterable = iterable if iterable else tuple()
        if default:
            self.dict = defaultdict(default)
            self.dict.update(iterable)
        else:
            self.dict = dict(iterable)

    def get(self, k, default=None):
        return self.dict.get(k, default)


    def items(self):
        for k, v in self.dict.items():
            yield k, v

    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, key, value):
        History.push_action(DictSetAction(self.dict, key, value))
        self.dict[key] = value

    def __len__(self):
        return len(self.dict)

    def __delitem__(self, key):
        History.push_action(DictRemoveAction(self.dict, key))
        del self.dict[key]

    def __eq__(self, other):
        return self.dict == other.dict

