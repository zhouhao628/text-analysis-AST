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
    tex