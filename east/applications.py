# -*- coding: utf-8 -*

import itertools
import sys

from east import consts
from east import logging
from east import relevance
from east import utils

def keyphrases_table(keyphrases, texts, similarity_measure=None, synonimizer=None,
                     language=consts.Language.ENGLISH):
    """
    Constructs the keyphrases table, containing thei