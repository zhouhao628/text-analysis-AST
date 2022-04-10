# -*- coding: utf-8 -*

from east.asts import ast
from east.asts import utils
from east import consts


class NaiveAnnotatedSuffixTree(ast.AnnotatedSuffixTree):

    __algorithm__ = consts.ASTAlgorithm.AST_NAIVE

    def _construct(self, strings_collection):
        """
        Naive generalized suffix tree construction algorithm,
        with quadratic [O(n_1^2 + ... + n_m^2)] worst-case time complexity,
        where m is the number of strings in collection.
        
        """
        
        # 0. Add a unique character to each string in the collection,
        #    to preserve simplicity while building the tree
        strings_collection = utils.make_unique_endings(strings_collection)
        
        root = ast.AnnotatedSuffixTree.Node()