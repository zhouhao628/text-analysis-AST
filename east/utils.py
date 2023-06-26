# -*- coding: utf-8 -*

import itertools
import os
import random
import re
import sys

from nltk.corpus import stopwords as nltk_stopwords


class ImmutableMixin(object):
    _inited = False

    def __init__(self):
        self._inited = True

    def __setattr__(self, key, value):
        if self._inited:
            raise exceptions.ImmutableException()
        super(ImmutableMixin, self).__setattr__(key, value)


class EnumMixin(object):
    def __iter__(self):
        for k, v in itertools.imap(lambda x: (x, getattr(self, x)), dir(self)):
            if not k.startswith('_'):
                yield v


def prepare_text(text):
    text = unicode(text.decode('utf-8', errors='replace'))
    text = text.upper()
    return text


def tokenize(text):
    return re.findall(re.compile("[\w']+", re.U), text)


def tokenize_and_filter(text, min_word_length=3, stopwords=None):
    tokens = tokenize(text)
    # TODO(mikhaildubov): Add language detection
    stopwords = stopwords or set(word.upper() for word in nltk_stopwords.words("english"))
    return [token for token in tokens
            if len(token) >= min_word_length and token not in stopwords]


def text_to_strings_collection(text, words=3):
    """
    Splits the text to a collection of strings;
    a GAST for such a split collection usually produces
    better results in keyword matching that a GAST
    for the whole text. The word parameters determines
    how many words each string in the collection shall
    consist of (3 by default)
    
    return: Unicode
    """
    
    text = prepare_text(text)
    strings_collection = tokenize(text)
    strings_collection = filter(lambda s: len(s) > 2 and not s.isdigit(), strings_collection)
        
    i = 0
    strings_collection_grouped = []
    while i < len(strings_collection):
        group = ''
        for j in xrange(words):
            if i + j < len(strings_collection):
              