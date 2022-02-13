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
    :param texts: dictionary of form {text_name: text}
    :param similarity_measure: similarity measure to use
    :param synonimizer: SynonymExtractor object to be used
    :param language: Language of the text collection / keyphrases

    :returns: dictionary of dictionaries, having keyphrases on its first level and texts
              on the second level.
    """

    similarity_measure = similarity_measure or relevance.ASTRelevanceMeasure()

    text_titles = texts.keys()
    text_collection = texts.values()
    similarity_measure.set_text_collection(text_collection, language)

    i = 0
    keyphrases_prepared = {keyphrase: utils.prepare_text(keyphrase)
                           for keyphrase in keyphrases}
    total_keyphrases = len(keyphrases)
    total_scores = len(text_collection) * total_keyphrases
    res = {}
    for keyphrase in keyphrases:
        if not keyphrase:
            continue
        res[keyphrase] = {}
        for j in xrange(len(text_collection)):
            i += 1
            logging.progress("Calculating matching scores", i, total_scores)
            res[keyphrase][text_titles[j]] = similarity_measure.relevance(
                                                        keyphrases_prepared[keyphrase],
                                                        text=j, synonimizer=synonimizer)

    logging.clear()

    return res


def keyphrases_graph(keyphrases, texts, referral_confidence=0.6, relev