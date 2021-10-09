# -*- coding: utf-8 -*

import getopt
import sys

from east.synonyms import synonyms

def main(args):
    opts, args = getopt.getopt(args, "")

    path = args[0]

    synonimizer = synonyms.SynonymExtractor(path)
    print "Prepared synonimizer\n"

    synonym_dicts = synonimizer.get_s