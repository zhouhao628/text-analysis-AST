# -*- coding: utf-8 -*

from east import consts


def index(array, key, start=0):
    # NOTE(msdubov): No boundary check for optimization purposes.
    i = start
    while array[i] != key:
        i += 1
    return i


def match_strings(str1, str2):
    """
    Returns t