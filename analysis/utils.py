# -*- coding: utf-8 -*

from east import utils

def worst_case_strings_collection(m, n):
    # NOTE(msdubov): strings differ only in their last 2 symbols.
    prefix = utils.random_stri