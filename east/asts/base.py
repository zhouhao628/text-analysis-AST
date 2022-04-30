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
        for ast_cls in utils.itersubclasses(AST):
            if not inspect.isabstract(ast_cls) and ast_algorithm == ast_cls.__algorithm__:
                return ast_cls(strings_collection)
        raise exceptions.NoSuchASTAlgorithm(name=ast_algorithm)

    def __init__(self, strings_collection):
        if not strings_collection:
            raise except