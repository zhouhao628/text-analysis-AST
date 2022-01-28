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
    Constructs the keyphrases table, containing their matching scores in a set of texts.

    The resulting table is stored as a dictionary of dictionaries,
    where the entry table["keyphrase"]["text"] corresponds
    to the matching score (0 <= score <= 1) of keyphrase "keyphrase"
    in the text named "text".
    
    :param keyphrases: list of strings
    :param texts: dictiona