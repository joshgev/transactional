__author__ = 'jgevirtz'
import random
from transactional.structures import Set
from transactional.core import Transaction
from unittest import TestCase

class TestSetBasic(TestCase):
    def test_uniqueness(self):
        """
        Make sure the set itself works
        """
        s1 = Set()
        s1.add(1)
        s1.add(1)
        s1.add(2)

        s2 = Set()
        s2.add(1)
        s2.add(2)
        assert s1 == s2

    def test_init(self):
        s1 = Set([1, 2, 3, 3])
        s2 = Set()
        s2.add(1)
        s2.add(1)
        s2.add(2)
        s2.add(3)
        s2.add(3)

        assert s1 == s2

    def test_remove(self):
        s1 = Set([0, 1, 2, 3, 4])
        s = {0, 1, 2, 3, 4}
        for i in range(5):
            s1.remove(i)
            s.remove(i)
            assert s1 == Set(s)

    def test_iter(self):
        s = Set([0, 1, 2, 3, 4, 5])
        assert [i for i in s] == [i for i in range(6)]

    def test_diff(self):
        s1 = Set([0, 1, 2, 3, 4])
        s2 = Set([2, 3])
        s3 = Set([0, 1, 4])
        assert (s1 - s2) == s3

    def test_intersection(self):
        s1 = Set([0, 1, 2])
        s2 = Set([0, 2, 3, 4])
        s3 = Set([0, 2])
        assert (s1 & s2) == s3

    def test_union(self):
        s1 = Set([0, 1, 2])
        s2 = Set([3, 4, 5])
        s3 = Set(i for i in range(6))

        assert (s1 | s2) == s3


class TestSetTransactional(TestCase):
    def setUp(self):
        random.seed(1987)

    def test(self):
        s = Set()
        with Transaction() as t1:
            for i in range(1000):
                s.add(random.randint(0, 50))
        s_copy1 = Set(s)

        with Transaction() as t2:
            for i in range(1000):
                s.add(random.randint(0, 50))
        s_copy2 = Set(s)

        t2.undo()
        assert s == s_copy1

        t2.do()
        assert s == s_copy2

        t2.undo()
        t1.undo()

        assert s == Set()

