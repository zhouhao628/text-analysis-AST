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
        root.strings_collection = strings_collection
        
        # For each string in the collection...
        for string_ind in xrange(len(strings_collection)):
            string = strings_collection[string_ind]
            # For each suffix of that string...
            # (do not handle unique last characters as suffixes)
            for suffix_start in xrange(len(string)-1):
                suffix = string[suffix_start:]
       