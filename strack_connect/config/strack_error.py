# :coding: utf-8
# :copyright: Copyright (c) 2021 strack


class StrackError(RuntimeError):
    """ Custom error class. """

    def __init__(self, arg):
        self.args = arg
