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

    def relevance(self, keyphrase, text, 