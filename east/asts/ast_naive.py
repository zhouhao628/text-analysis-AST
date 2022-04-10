# -*- coding: utf-8 -*

from east.asts import ast
from east.asts import utils
from east import consts


class NaiveAnnotatedSuffixTree(ast.AnnotatedSuffixTree):

    __algorithm__ = consts.ASTAlgorithm.AST_NAIVE

    def _construct(self, strings_collect