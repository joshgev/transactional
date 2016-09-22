__author__ = 'jgevirtz'

import random
from transactional.core import Transaction, Variable
from unittest import TestCase



class TestVariable(TestCase):
    def setUp(self):
        random.seed(1987)

    def test(self):
        l = [Variable(i) for i in range(100)]
        with Transaction() as t1:
            for i in range(1000):
                index = random.randint(0, 99)
                l[index](i)
        vals = [v() for v in l]
        assert vals != [i for i in range(100)]

        t1.undo()
        vals = [v() for v in l]
        assert vals == [i for i in range(100)]
