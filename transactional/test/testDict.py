__author__ = 'jgevirtz'

import random
from transactional.structures import Dict
from transactional.core import Transaction
from unittest import TestCase


class TestDictBasic(TestCase):
    def test_basic(self):
        d = Dict()
        d["a"] = 1
        d["b"] = 2

        assert len(d) == 2
        assert d["a"] == 1
        assert d["b"] == 2

    def test_delete(self):
        d = Dict()
        d["a"] = 1
        del d["a"]
        assert len(d) == 0

    def test_replace(self):
        d = Dict()
        d["a"] = 1
        assert d["a"] == 1
        d["a"] = 2
        assert d["a"] == 2
        assert len(d) == 1

    def test_init(self):
        data = (
            ("a", 1),
            ("b", 2),
            ("c", 3),
            ("d", 4),
            ("e", 5),
            ("e", 6) # Note the duplicate key
        )
        d = Dict(data)
        assert len(d) == 5
        assert d["a"] == 1
        assert d["b"] == 2
        assert d["c"] == 3
        assert d["d"] == 4
        assert d["e"] == 6

    def test_items(self):
        data = [(i, i**2) for i in range(10)]
        d = Dict(data)
        for i, (k, v) in zip(range(10), d.items()):
            assert k == i and v == i ** 2

class TestDictTransactional(TestCase):
    def setUp(self):
        random.seed(1987)

    def test(self):
        d = Dict()

        with Transaction() as t1:
            for i in range(10):
                d[random.randint(0, 100)] = random.randint(0, 1000)

        d_copy1 = Dict(d.items())

        with Transaction() as t2:
            for i in range(10):
                d[random.randint(0, 100)] = random.randint(0, 1000)

        d_copy2 = Dict(d.items())

        t2.undo()
        assert d == d_copy1

        t2.do()
        print (d_copy2.dict)
        print (d.dict)
        assert d == d_copy2, len(d)

        t2.undo()
        t1.undo()

        assert d == Dict()


