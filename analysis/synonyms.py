# -*- coding: utf-8 -*

import getopt
import sys

from east.synonyms import synonyms

def main(args):
    opts, args = getopt.getopt(args, "")

    path = args[0]

    synonimizer = synonyms.SynonymExtractor(path)
    print "Prepared synonimizer\n"

    synonym_dicts = synonimizer.get_synonyms(threshold=0.3, return_similarity_measure=True)
    for w1 in synonym_dicts:
        syn_str = ["%s (%.2f)" % (w2, sim) for w2, sim in syn