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
    Returns the largest index i such that str1[:i] == str2[:i]
    
    """
    i = 0
    min_len = len(str1) if len(str1) < len(str2) else len(str2)
    while i < min_len and str1[i] == str2[i]: i += 1
    return i


def make_unique_endings(strings_collection):
    """
    Make each string in the collectio