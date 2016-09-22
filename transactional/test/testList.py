__author__ = 'jgevirtz'

import random
from transactional.structures import List
from transactional.core import Transaction
from unittest import TestCase


class TestListBasic(TestCase):
    def test_init(self):
        l = List(range(100))
        print(l.list)
        for i in range(100):
            print(l[i])
            assert l[i] == i, i - l[i]

    def test_append(self):
        l = List()
        assert len(l) == 0
        for i in range(100):
            l.append(i)
        assert l == List(range(100))

    def test_pop(self):
        l = List(range(100))
        for i in range(99, 0, -1):
            assert l.pop() == i

    def test_add(self):
        l1 = List(range(0, 50))
        l2 = List(range(50, 100))
        assert l1 + l2 == List(range(100))

    def test_iter(self):
        l = List(range(100))
        for i, j in zip(l, range(100)):
            assert i == j


class TestListTransactional(TestCase):
    def setUp(self):
        random.seed(1987)

    def test(self):
        l = List()

        with Transaction() as t1:
            for i in range(1000):
                l.append(random.randint(0, 50))

        l_copy1 = List(l)

        with Transaction() as t2:
            for i in range(1000):
                l.append(random.randint(0, 50))

        l_copy2 = List(l)

        t2.undo()
        assert l == l_copy1

        t2.do()
        assert l == l_copy2

        t2.undo()
        t1.undo()
        assert l == List()

