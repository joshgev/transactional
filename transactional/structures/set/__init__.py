__author__ = 'jgevirtz'

from .actions import *
from ...core import History


class Set(object):
    def __init__(self, iterable=tuple()):
        self._set = set(iterable)

    def add(self, item):
        History.push_action(SetAddAction(self._set, item))
        self._set.add(item)

    def remove(self, item):
        # TODO: Definitely need try/catch to junk History.current_activity if we get an exception
        History.push_action(SetRemoveAction(self._set, item))
        self._set.remove(item)

    def __and__(self, other):
        if isinstance(other, set):
            return Set(self._set & other)
        else:
            return Set(self._set & other._set)

    def __or__(self, other):
        if isinstance(other, set):
            return Set(self._set | other)
        else:
            return Set(self._set | other._set)

    def __sub__(self, other):
        if isinstance(other, set):
            return Set(self._set - other)
        else:
            return Set(self._set - other._set)

    def __iter__(self):
        for i in self._set:
            yield i

    def __str__(self):
        return "Set({})".format(",".join(str(i) for i in self._set))

    def __len__(self):
        return len(self._set)

    def __eq__(self, other):
        return self._set == other._set