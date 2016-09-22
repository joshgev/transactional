__author__ = 'jgevirtz'


class AncestorException(Exception):
    def __init__(self, msg):
        super(AncestorException, self).__init__(msg)