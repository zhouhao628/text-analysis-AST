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
        self.words = set([dt[0] for dt in self.dependency_triples] +
                         [dt[2] for dt in self.dependency_triples])
        self.relations = set([dt[1] for dt in self.dependency_triples])
        self.I_memoized = {}
        self.T_memoized = {}
        self.synonyms_memoized = {}

    def _retrieve_text(self, input_path):
        if os.path.isdir(input_path):
            text = ""
            number_of_texts = 0
            for file_name in os.listdir(input_path):
                if file_name.endswith(".txt"):
                    with open(os.path.abspath(input_path) + "/" + file_name) as f:
                        text += f.read()
                        number_of_texts += 1
        else:
            with open(input_path) as f:
                text = f.read()
                number_of_texts = 1
        return text, number_of_texts

    def _retrieve_dependency_triples(self, text):

        dependency_triples = []

        # Additional indexes to speed up the calculation of I(w1, r, w2)
        dt_for_r = collections.defaultdict(list)
        dt_for_w1r = collections.defaultdict(list)
        dt_for_rw2 = collections.defaultdict(list)

        p = subprocess.Popen([self.tomita_binary, "c