
# -*- coding: utf-8 -*

import itertools
import numpy as np

from east.asts import base
from east.asts import utils
from east import consts
from east import utils as common_utils


class EnhancedAnnotatedSuffixArray(base.AST):

    __algorithm__ = consts.ASTAlgorithm.EASA

    def __init__(self, strings_collection):
        super(EnhancedAnnotatedSuffixArray, self).__init__(strings_collection)
        self.strings_collection = strings_collection
        self.string = "".join(utils.make_unique_endings(strings_collection))
        self.suftab = self._compute_suftab(self.string)
        self.lcptab = self._compute_lcptab(self.string, self.suftab)
        self.childtab_up, self.childtab_down = self._compute_childtab(self.lcptab)
        self.childtab_next_l_index = self._compute_childtab_next_l_index(self.lcptab)
        self.anntab = self._compute_anntab(self.suftab, self.lcptab)

    def score(self, query, normalized=True, synonimizer=None, return_suffix_scores=False):
        if synonimizer:
            synonyms = synonimizer.get_synonyms()
            query_words = common_utils.tokenize(query)
            for i in xrange(len(query_words)):
                query_words[i] = synonyms[query_words[i]] + [query_words[i]]
            possible_queries = map(lambda words: "".join(words),
                                   itertools.product(*query_words))
            return max(self._score(q) for q in possible_queries)
        else:
            return self._score(query.replace(" ", ""), normalized, return_suffix_scores)

    def traverse_depth_first_pre_order(self, callback):
        """Visits the internal "nodes" of the enhanced suffix array in depth-first pre-order.

        Based on Abouelhoda et al. (2004).
        """
        n = len(self.suftab)
        root = [0, 0, n - 1, ""]  # <l, i, j, char>

        def _traverse_top_down(interval):  # TODO: Rewrite with stack? As in bottom-up
            callback(interval)
            i, j = interval[1], interval[2]
            if i != j:
                children = self._get_child_intervals(i, j)