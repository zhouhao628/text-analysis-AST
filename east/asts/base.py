# -*- coding: utf-8 -*

import abc
import inspect

from east import consts
from east import exceptions
from east import utils

class AST(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def get_ast(strings_collection, ast_algorithm="easa"):
        for ast_cls in utils.iters