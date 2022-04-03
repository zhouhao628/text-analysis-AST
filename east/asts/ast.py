
# -*- coding: utf-8 -*

import abc

from east.asts import base
from east.asts import utils
from east import consts


class AnnotatedSuffixTree(base.AST):
    __metaclass__ = abc.ABCMeta

    def __init__(self, strings_collection):
        super(AnnotatedSuffixTree, self).__init__(strings_collection)
        self.strings_collection = strings_collection
        self.root = self._construct(strings_collection)
        self._update_node_depth()

    def score(self, query, normalized=True, synonimizer=None, return_suffix_scores=False):
        """
        Matches the string against the GAST using
        the algorithm described in [Chernyak, sections 1.3 & 1.4].
        
        Expects the input string to consist of