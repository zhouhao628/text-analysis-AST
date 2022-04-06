
# -*- coding: utf-8 -*

from east.asts import ast
from east.asts import utils
from east import consts


class LinearAnnotatedSuffixTree(ast.AnnotatedSuffixTree):

    __algorithm__ = consts.ASTAlgorithm.AST_LINEAR

    def _construct(self, strings_collection):
        """
        Generalized suffix tree construction algorithm based on the
        Ukkonen's algorithm for suffix tree construction,
        with linear [O(n_1 + ... + n_m)] worst-case time complexity,
        where m is the number of strings in collection.
        
        """
        
        # 1. Add a unique character to each string in the collection
        strings_collection = utils.make_unique_endings(strings_collection)
    
        ############################################################
        # 2. Build the GST using modified Ukkonnen's algorithm     #
        ############################################################
        
        root = ast.AnnotatedSuffixTree.Node()
        root.strings_collection = strings_collection
        # To preserve simplicity
        root.suffix_link = root
        root._arc = (0,-1,0)
        # For constant updating of all leafs, see [Gusfield {RUS}, p. 139]
        root._e = [0 for _ in xrange(len(strings_collection))]
        
        
        def _ukkonen_first_phases(string_ind):
            """
            Looks for the part of the string which is already encoded.
            Returns a tuple of form
            ([length of already encoded string preffix],
             [tree node to start the first explicit phase with],
             [path to go down at the beginning of the first explicit phase]).
            
            """
            already_in_tree = 0
            suffix = strings_collection[string_ind]
            starting_path = (0, 0, 0)
            starting_node = root
            child_node = starting_node.chose_arc(suffix)
            while child_node:
                (str_ind, substr_start, substr_end) = child_node.arc()
                match = utils.match_strings(
                            suffix, strings_collection[str_ind][substr_start:substr_end])
                already_in_tree += match
                if match == substr_end-substr_start:
                    # matched the arc, proceed with child node
                    suffix = suffix[match:]
                    starting_node = child_node
                    child_node = starting_node.chose_arc(suffix)
                else:
                    # otherwise we will have to proceed certain path at the beginning
                    # of the first explicit phase
                    starting_path = (str_ind, substr_start, substr_start+match)
                    break
            # For constant updating of all leafs, see [Gusfield {RUS}, p. 139]
            root._e[string_ind] = already_in_tree
                
            return (already_in_tree, starting_node, starting_path)
        
        def _ukkonen_phase(string_ind, phase, starting_node, starting_path, starting_continuation):
            """
            Ukkonen's algorithm single phase.
            Returns a tuple of form:
            ([tree node to start the next phase with],
             [path to go down at the beginning of the next phase],
             [starting continuation for the next phase]).
            
            """
            current_suffix_end = starting_node
            suffix_link_source_node = None
            path_str_ind, path_substr_start, path_substr_end = starting_path
            # Continuations [starting_continuation..(i+1)]
            for continuation in xrange(starting_continuation, phase+1):
                # Go up to the first node with suffix link [no more than 1 pass]
                if continuation > starting_continuation:
                    path_str_ind, path_substr_start, path_substr_end = 0, 0, 0
                    if not current_suffix_end.suffix_link:
                        (path_str_ind, path_substr_start, path_substr_end) = current_suffix_end.arc()
                        current_suffix_end = current_suffix_end.parent
                    if current_suffix_end.is_root():
                        path_str_ind = string_ind
                        path_substr_start = continuation
                        path_substr_end = phase
                    else:
                        # Go through the suffix link
                        current_suffix_end = current_suffix_end.suffix_link
                        
                # Go down the path (str_ind, substr_start, substr_end)
                # NB: using Skip/Count trick,
                # see [Gusfield {RUS} p.134] for details
                g = path_substr_end - path_substr_start
                if g > 0:
                    current_suffix_end = current_suffix_end.chose_arc(strings_collection
                                         [path_str_ind][path_substr_start])
                (_, cs_ss_start, cs_ss_end) = current_suffix_end.arc()
                g_ = cs_ss_end - cs_ss_start
                while g >= g_:
                    path_substr_start += g_
                    g -= g_
                    if g > 0:
                        current_suffix_end = current_suffix_end.chose_arc(strings_collection
                                             [path_str_ind][path_substr_start])
                    (_, cs_ss_start, cs_ss_end) = current_suffix_end.arc()
                    g_ = cs_ss_end - cs_ss_start
                    
                # Perform continuation by one of three rules,
                # see [Gusfield {RUS} p. 129] for details
                if g == 0:
                    # Rule 1
                    if current_suffix_end.is_leaf():
                        pass
                    # Rule 2a
                    elif not current_suffix_end.chose_arc(strings_collection[string_ind][phase]):
                        if suffix_link_source_node:
                            suffix_link_source_node.suffix_link = current_suffix_end
                        new_leaf = current_suffix_end.add_new_child(string_ind, phase, -1)
                        new_leaf.weight = 1
                        if continuation == starting_continuation:
                            starting_node = new_leaf
                            starting_path = (0, 0, 0)
                    # Rule 3a
                    else:
                        if suffix_link_source_node:
                            suffix_link_source_node.suffix_link = current_suffix_end
                        starting_continuation = continuation
                        starting_node = current_suffix_end
                        starting_path = (string_ind, phase, phase+1)
                        break
                    suffix_link_source_node = None
                else:
                    (si, ss, se) = current_suffix_end._arc
                    # Rule 2b
                    if strings_collection[si][ss + g] != strings_collection[string_ind][phase]:
                        parent = current_suffix_end.parent
                        parent.remove_child(current_suffix_end)
                        current_suffix_end._arc = (si, ss+g, se)
                        new_node = parent.add_new_child(si, ss, ss + g)
                        new_leaf = new_node.add_new_child(string_ind, phase, -1)
                        new_leaf.weight = 1
                        if continuation == starting_continuation:
                            starting_node = new_leaf
                            starting_path = (0, 0, 0)
                        new_node.add_child(current_suffix_end)
                        if suffix_link_source_node:
                            # Define new suffix link