# -*- coding: utf-8 -*

from east import consts


class EastException(Exception):
    """Base EAST Exception.

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.
    """
    msg_fmt = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs)