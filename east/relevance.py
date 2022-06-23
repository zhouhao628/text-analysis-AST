# -*- coding: utf-8 -*

from collections import defaultdict
import math
import sys

from nltk.stem import snowball
import numpy as np

from east.asts import base
from east import consts
from east import logging
from east import utils


class RelevanceMeasure(object):

    def set_text_collection(self, texts, language=consts.Language.ENGLISH):
        raise NotImplemented()

    def relevance(self, keyphrase, text, synonimizer=None):
        # text is the index of the text to measure the relevance to
        # TODO(mikhaildubov): Add detailed docstrings