# -*- coding: utf-8 -*

import itertools
import os
import random
import re
import sys

from nltk.corpus import stopwords as nltk_stopwords


class ImmutableMixin(object):
    _in