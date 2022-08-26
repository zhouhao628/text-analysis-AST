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
        raise NotImplemented()


class ASTRelevanceMeasure(RelevanceMeasure):

    def __init__(self, ast_algorithm=consts.ASTAlgorithm.EASA, normalized=True):
        super(ASTRelevanceMeasure, self).__init__()
        self.ast_algorithm = ast_algorithm
        self.normalized = normalized

    def set_text_collection(self, texts, language=consts.Language.ENGLISH):
        self.texts = texts
        self.language = language

        self.asts = []
        total_texts = len(texts)

        for i in xrange(total_texts):
            # NOTE(mikhaildubov): utils.text_to_strings_collection()
            #                     does utils.prepare_text() as well.
            self.asts.append(base.AST.get_ast(
                                    utils.text_to_strings_collection(texts[i]),
                                    self.ast_algorithm))
            logging.progress("Indexing texts with ASTs", i + 1, total_texts)

        logging.clear()

    def relevance(self, keyphrase, text, synonimizer=None):
        return self.asts[text].score(keyphrase, normalized=self.normalized,
                                     synonimizer=synonimizer)


class CosineRelevanceMeasure(RelevanceMeasure):

    def __init__(self, vector_space=consts.VectorSpace.STEMS,
                 term_weighting=consts.TermWeighting.TF_IDF):
        super(CosineRelevanceMeasure, self).__init__()
        self.vector_space = vector_space
        self.term_weighting = term_weighting
        

    def set_text_collection(self, texts, language=consts.Language.ENGLISH):
        self.language = language
        if self.vector_space == consts.VectorSpace.STEMS:
            self.stemmer = snowball.SnowballStemmer(self.language)
        raw_tokens = []
        total_texts = len(texts)
        for i in xrange(total_t