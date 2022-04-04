
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
        alphabet letters only (no whitespaces etc.)
        
        Returns the score (a float in [0, 1]).
        
        query -- Unicode
        
        """
        
        query = query.replace(" ", "")
        result = 0
        suffix_scores = {}
    
        # For each suffix of the string:
        for suffix_start in xrange(len(query)):
            
            suffix = query[suffix_start:]
            suffix_score = 0
            suffix_result = 0
            matched_chars = 0
            nodes_matched = 0
            
            child_node = self.root.chose_arc(suffix)
            while child_node:
                nodes_matched += 1
                (str_ind, substr_start, substr_end) = child_node.arc()
                match = utils.match_strings(
                            suffix, self.strings_collection[str_ind][substr_start:substr_end])
                suffix_score += child_node.conditional_probability()
                matched_chars += match
                suffix = suffix[match:]
                if suffix and match == substr_end - substr_start:
                    child_node = child_node.chose_arc(suffix)
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

    def traverse_depth_first_pre_order(self, callback):
        """Traverses the annotated suffix tree in depth-first pre-order."""
        self.root.traverse_depth_first_pre_order(callback)

    def traverse_depth_first_post_order(self, callback):
        """Traverses the annotated suffix tree in depth-first post-order."""
        self.root.traverse_depth_first_post_order(callback)

    def traverse_breadth_first(self, callback):
        """Traverses the annotated suffix tree in breadth-first order."""
        self.root.traverse_breadth_first(callback, [])

    @abc.abstractmethod
    def _construct(self, strings_collection):
        """Constructs the annotated suffix tree and returns the pointer to its root."""
    
    def _update_node_depth(self):
        self.root.depth = 0
        def _calculate_depth(node):
            for k in node.children:
                node.children[k].depth = node.depth + 1
        self.traverse(_calculate_depth, consts.TraversalOrder.DEPTH_FIRST_PRE_ORDER)

    class Node:
        """
        Implementation of a Generalized Annotated Suffix Tree node.
        
        """ 
            
        def __init__(self):
            """ Hash table to store child nodes """
            self.children = {}
            """ Node weight """
            self.weight = 0
            """ Parent """
            self.parent = None
            """ Suffix link """
            self.suffix_link = None
            """ Arc that points to the node; Triple of form
                (string_index, substring_start_index[inclusive], substring_end_index[exclusive]) """
            self._arc = None
            """ Used in Ukkonen's algorithm """
            self._e = []
            """ Pointer to the strings collection """
            self.strings_collection = []
            # No sense in initializing node weight here
            # it is not possible to update it quickly while
            # constructing the tree; that's made later in one single pass
                
        
        def add_new_child(self, str_ind, substr_start, substr_end):
            """
            Creates and returns new child node.
            str_ind, substr_start, substr_end and parameters describe
            the substring that the new child should contain;
            for the given strings_collection that will be
            strings_collection[str_ind][substr_start:substr_end]
            
            """
            child_node = AnnotatedSuffixTree.Node()
            child_node.parent = self
            child_node.strings_collection = self.strings_collection
            child_node._arc = (str_ind, substr_start, substr_end)
            child_node._e = self._e
            self.children[self.strings_collection[str_ind][substr_start]] = child_node
            return child_node
        
        
        def add_child(self, child_node):
            """
            Adds an existing node as a new child
            for the current node.
            
            """
            (str_ind, substr_start, _) = child_node.arc()
            child_node.strings_collection = self.strings_collection
            self.children[self.strings_collection[str_ind][substr_start]] = child_node
            child_node.parent = self
        
        
        def remove_child(self, child_node):
            """
            Removes a child node from the current node.
            
            """
            (str_ind, substr_start, _) = child_node.arc()
            del self.children[self.strings_collection[str_ind][substr_start]]
            
            
        def conditional_probability(self):
            """