# -*- coding: utf-8 -*

import codecs
import collections
import itertools
import math
import os
import subprocess
from xml.dom import minidom


from east import consts
from east import exceptions
from east import utils as common_utils
from east.synonyms import utils


class SynonymExtractor(object):

    def __init__(self, input_path):
        self.current_os = utils.determine_operating_system()
        self.tomita_path, self.tomita_binary = self._get_tomita_path()
        if self.tomita_binary is None:
            raise exceptions.TomitaNotInstalledException()
        self.text, self.number_of_texts = self._retrieve_text(input_path)
        self.dependency_triples, self.dt_for_r, self.dt_for_w1r, self.dt_for_rw2 = \
            self._retrieve_dependency_triples(self.text)
        self.word_frequencies = self._calculate_word_frequencies(self.text)
        self.frequencies = self._calculate_dt_frequencies(self.dependency_triples)
        self.wor