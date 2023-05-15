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
        if 