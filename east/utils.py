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
            raise exception