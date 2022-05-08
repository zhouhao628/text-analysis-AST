
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
                children.sort(key=lambda child: child[3])
                for child in children:
                    _traverse_top_down(child)

        _traverse_top_down(root)

    def traverse_depth_first_post_order(self, callback):
        """Visits the internal "nodes" of the enhanced suffix array in depth-first post-order.

        Kasai et. al. (2001), Abouelhoda et al. (2004).
        """
        # a. Reimplement without python lists?..
        # b. Interface will require it to have not internal nodes only?..
        #    (but actually this implementation gives a ~2x gain of performance)
        last_interval = None
        n = len(self.suftab)
        stack = [[0, 0, None, []]]  # <l, i, j, children>
        for i in xrange(1, n):
            lb = i - 1
            while self.lcptab[i] < stack[-1][0]:
                stack[-1][2] = i - 1
                last_interval = stack.pop()
                callback(last_interval)
                lb = last_interval[1]
                if self.lcptab[i] <= stack[-1][0]:
                    stack[-1][3].append(last_interval)
                    last_interval = None
            if self.lcptab[i] > stack[-1][0]:
                if last_interval:
                    stack.append([self.lcptab[i], lb, None, [last_interval]])
                    last_interval = None
                else:
                    stack.append([self.lcptab[i], lb, None, []])
        stack[-1][2] = n - 1
        callback(stack[-1])

    def traverse_breadth_first(self, callback):
        """Visits the internal "nodes" of the enhanced suffix array in breadth-first order."""
        raise NotImplementedError

    def _score(self, query, normalized=True, return_suffix_scores=False):
        result = 0
        suffix_scores = {}
        n = len(self.suftab)

        root_interval = (0, 0, n - 1)
    
        for suffix_start in xrange(len(query)):
            
            suffix = query[suffix_start:]
            suffix_score = 0
            suffix_result = 0
            matched_chars = 0
            nodes_matched = 0
            
            parent_node = root_interval
            child_node = self._get_child_interval(parent_node[1], parent_node[2], suffix[0])
            while child_node:
                nodes_matched += 1
                # TODO: Use structs??? child_node[1] is actually cn.i; parent_node[0] == pn.l
                substr_start = self.suftab[child_node[1]] + parent_node[0]
                if self._is_leaf(child_node):
                    substr_end = n
                else:
                    substr_end = substr_start + child_node[0] - parent_node[0]
                match = utils.match_strings(suffix, self.string[substr_start:substr_end])
                suffix_score += float(self._annotation(child_node)) / self._annotation(parent_node)
                matched_chars += match
                suffix = suffix[match:]
                if suffix and match == substr_end - substr_start:
                    parent_node = child_node
                    child_node = self._get_child_interval(parent_node[1], parent_node[2], suffix[0])
                else:
                    break

            if matched_chars:
                suffix_result = (suffix_score + matched_chars - nodes_matched)
                if normalized:
                    suffix_result /= matched_chars
                result += suffix_result

            suffix_scores[query[suffix_start:]] = suffix_result
            
        result /= len(query)

        if return_suffix_scores:
            result = result, suffix_scores

        return result

    def _compute_suftab(self, string):
        """Computes the suffix array of a string in O(n).

        The code is based on that from the pysuffix library (https://code.google.com/p/pysuffix/).

        Kärkkäinen & Sanders (2003).
        """
        n = len(string)
        string += (unichr(1) * 3)
        suftab = np.zeros(n, dtype=np.int)
        alpha = sorted(set(string))
        self._kark_sort(string, suftab, n, alpha)
        return suftab

    def _kark_sort(self, s, SA, n, alpha):
        n0 = (n + 2) / 3
        n1 = (n + 1) / 3
        n2 = n / 3
        n02 = n0 + n2

        SA12 = [0] * (n02 + 3)
        SA0 = [0] * n0
        s12 = [i for i in xrange(n + n0 - n1) if i % 3 != 0] + [0, 0, 0]

        self._radixpass(s12, SA12, s[2:], n02, alpha)
        self._radixpass(SA12, s12, s[1:], n02, alpha)
        self._radixpass(s12, SA12, s, n02, alpha)
  
        name = 0
        c0, c1, c2 = -1, -1, -1
        array_name = [0]
        for i in xrange(n02):
            if s[SA12[i]] != c0 or s[SA12[i] + 1] != c1 or s[SA12[i] + 2] != c2:
                name += 1
                array_name.append(name)
                c0 = s[SA12[i]]
                c1 = s[SA12[i]+1]
                c2 = s[SA12[i]+2]
            if SA12[i] % 3 == 1:
                s12[SA12[i] / 3] = name
            else:
                s12[SA12[i] / 3 + n0] = name

        if name < n02:
            self._kark_sort(s12, SA12, n02, array_name)
            for i in xrange(n02): 
                s12[SA12[i]] = i+1
        else:
            for i in xrange(n02): 
                SA12[s12[i]-1] = i

        s0 = [SA12[i] * 3 for i in xrange(n02) if SA12[i] < n0]

        self._radixpass(s0, SA0, s, n0, alpha)
  
        p = j = k = 0
        t = n0 - n1
        while k < n:
            i = SA12[t] * 3 + 1 if SA12[t] < n0 else (SA12[t] - n0) * 3 + 2
            j = SA0[p] if p < n0 else 0
 
            if SA12[t] < n0:
                test = (s12[SA12[t]+n0] <= s12[j/3]) if(s[i]==s[j]) else (s[i] < s[j])
            elif(s[i]==s[j]) :
                test = s12[SA12[t]-n0+1] <= s12[j/3 + n0] if(s[i+1]==s[j+1]) else s[i+1] < s[j+1]
            else:
                test = s[i] < s[j]

            if test:
                SA[k] = i
                t += 1
                if t == n02: 
                    k += 1
                    l = n0 - p
                    while p < n0:
                        SA[k] = SA0[p]
                        p += 1
                        k += 1          
            else: 